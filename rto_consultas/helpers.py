from django.db.models import Q, QuerySet, Subquery
from django.db.models import Model
from django.core.cache import cache
from datetime import timedelta, datetime


import re
from functools import reduce
from typing import Dict, List, Tuple, Set, Union
from dataclasses import dataclass, field

# from silk.profiling.profiler import silk_profile

from rto_consultas.models import (
    Certificados,
    Certificadosasignadosportaller,
    Talleres,
    Verificaciones,
    Verificacionespdf,
)
from .presigned_url import generate_presigned_url


@dataclass
class AuxData:
    query_fields: List[str]
    form_fields: Dict[str, Tuple[Union[str, None], Union[Model, None]]]
    parsed_names: Dict[str, str]
    ids: Dict[str, str] = field(default_factory=dict)
    types: Dict[str, str] = field(default_factory=dict)
    fecha_field: str = "fecha"
    aux: Dict[str, str] = field(default_factory=dict)


def convert_date(input_date):
    # Define the format of the input date
    input_format = "%b. %d, %Y"

    # Parse the input date string to a datetime object
    # date_obj = datetime.strptime(input_date, input_format)

    # Define the format of the output date
    output_format = "%d/%m/%Y"

    # Format the datetime object to the desired output format
    output_date = input_date.strftime(output_format)

    return output_date


def check_for_empty_query(query):
    def check_for_empty(val):
        match val:
            case "":
                return True
            case None:
                return True
            case _:
                return False

    return all([check_for_empty(val) for val in query.values()])


def handle_args(query_params, queryset, fecha_field="fecha"):
    numeric_test = re.compile(r"^\d+$")
    cleaned_query = clean_args(query_params)

    date_from = cleaned_query.pop("fecha_desde", None)
    date_to = cleaned_query.pop("fecha_hasta", None)
    if date_from or date_to:
        queryset = queryset.filter(handle_date_range(date_from, date_to, fecha_field))

    for key, arg in cleaned_query.items():
        if numeric_test.match(str(arg)):
            query = Q(**{f"{key}__exact": int(arg)})
        elif "dominio" in key:
            query = Q(**{f"{key}__exact": parse_license_plate(arg)})
        elif isinstance(arg, str):
            query = Q(**{f"{key}__icontains": arg})
        else:
            return queryset

        queryset = queryset.filter(query)

    return queryset


def handle_date_range(date_from, date_to, fecha_field="fecha"):
    if date_from and date_to:
        return Q(**{f"{fecha_field}__range": (date_from, date_to)})
    if date_from and not date_to:
        return Q(**{f"{fecha_field}__gte": date_from})


def clean_args(query_params):
    return {k: v for k, v in query_params.items() if v}


def parse_date(value):
    # Remove any non-digit characters from the input value
    value = value[0]
    digits_only = re.sub(r"\D", "", value)

    # Format the date as dd/mm/yyyy
    if len(digits_only) >= 8:
        formatted_value = re.sub(r"^(\d{2})(\d{2})(\d{4})$", r"\3-\2-\1", digits_only)
    elif len(digits_only) >= 4:
        formatted_value = re.sub(r"^(\d{2})(\d{2})(\d+)$", r"\3-\2-\1", digits_only)
    elif len(digits_only) >= 2:
        formatted_value = re.sub(r"^(\d{2})(\d+)$", r"\2-\1", digits_only)
    else:
        formatted_value = digits_only

    return formatted_value


def parse_license_plate(value):
    # Remove any non-alphanumeric characters from the input value
    # value = value[0]
    alphanumeric_only = re.sub(r"\W", "", value)

    # Format the license plate
    if len(alphanumeric_only) >= 7:
        formatted_value = re.sub(
            r"^(\w{2})(\d{3})(\w{2})$", r"\1-\2-\3", alphanumeric_only
        )
    elif len(alphanumeric_only) >= 6:
        formatted_value = re.sub(r"^(\w{3})(\d{3})$", r"\1-\2", alphanumeric_only)
    else:
        formatted_value = alphanumeric_only

    return formatted_value


def handle_query(request, model, fecha_field="fecha"):
    query = request.GET.copy()
    sort = query.pop("sort", None)
    page = query.pop("page", None)
    _export = query.pop("_export", None)
    nrocertificado = query.pop("nrocertificado", None)
    anulado = query.pop("anulado", None)

    cert_init = query.pop("cert_init", None)
    cert_end = query.pop("cert_end", None)

    handle_cert_insert(query.get("idtaller", None), cert_init, cert_end)

    queryset = handle_nrocertificado(nrocertificado, anulado, model)

    if not check_for_empty_query(query):
        queryset = handle_args(query, queryset, fecha_field=fecha_field)
    if sort:
        queryset = queryset.order_by(sort[0])

    queryset = handle_anulado(queryset, anulado, model)
    return queryset


def handle_cert_insert(taller_id, cert_init, cert_end):
    print("PARAMS TO HANDLE:", taller_id, cert_init, cert_end)
    if taller_id and cert_end and cert_init:
        taller_id = int(taller_id[0])
        taller = Talleres.objects.get(idtaller__iexact=taller_id)
        certs = [
            Certificadosasignadosportaller(
                nrocertificado=nro,
                idtaller=taller,
                fechacarga=datetime.today(),
                disponible=1,
                replicado=0,
            )
            for nro in range(int(cert_init[0]), int(cert_end[0]))
        ]

        Certificadosasignadosportaller.objects.bulk_create(certs)


def handle_form(data: AuxData, model: Model):
    values = {}
    for field in data.form_fields.keys():
        if data.form_fields[field][0]:
            try:
                val = model.objects.values_list(field, flat=True).distinct()
                values[field] = val
            except Exception as e:
                print(e)
                # Maybe the model is not a foreign key
                val = (
                    data.form_fields[field][1]
                    .objects.values_list("descripcion", flat=True)
                    .distinct()
                )
                values[field] = val

        else:
            values[field] = [0, 1]
    return values


def map_fields(data: AuxData, model: Model):
    values = {}

    for field, vals in data.form_fields.items():
        dfield, dmodel = vals
        if bool(dfield):
            dfield = vals[0]
            dmodel: Model = vals[1]

            cache_key = f"unique_values_{model._meta.db_table}_{field}"
            cached_values = cache.get(cache_key)

            if cached_values is None:
                try:
                    values_list = model.objects.values_list(field, flat=True).distinct()
                except Exception as e:
                    print(e)
                    values_list = dmodel.objects.values_list(
                        "descripcion", flat=True
                    ).distinct()

                descriptions = dmodel.objects.values_list(dfield, flat=True).distinct()
                vals = {v: d for v, d in zip(values_list, descriptions)}
                values[field] = vals

                cache.set(cache_key, vals)
            else:
                values[field] = cached_values

        else:
            values[field] = {0: "Falso", 1: "Verdadero"}

    return values


def handle_context(context, view):
    val_dict = handle_form(view.aux_data, view.model)
    context["form_fields"] = val_dict
    context["descriptions"] = map_fields(view.aux_data, view.model)
    context["parsed_fields"] = view.aux_data.parsed_names
    fields = view.model._meta.fields
    context["fields"] = fields
    # context["query_fields"] = list(filter(lambda x: x.name in view.query_fields and x.name not in view.form_fields, fields))
    context["query_fields"] = view.aux_data.query_fields
    context["ids"] = view.aux_data.ids
    context["types"] = view.aux_data.types
    context["aux"] = view.aux_data.aux
    return context


def handle_anulado(queryset, anulado, model):
    # _queryset = model.objects.all()
    # vals = {"Verdadero": 1, "Falso": 0}
    try:
        anulado = int(anulado[0])
    except:
        anulado = None

    print("ANULADO: ", anulado)
    match anulado:
        case [""]:
            return queryset
        case None:
            return queryset
        case _:
            certs = model.objects.filter(anulado__exact=anulado)
            qa = Q(
                idtaller_id__in=Subquery(certs.values("idtaller_id")),
            )
            qb = Q(
                idverificacion__in=Subquery(certs.values("idverificacion_id")),
            )
            verifs_segun_anulado = Verificaciones.objects.filter(qa & qb)
            final_q = queryset.intersection(verifs_segun_anulado)
            return final_q


def handle_nrocertificado(nrocertificado, anulado, model):
    queryset = model.objects.all()

    print(model)

    match nrocertificado:
        case [""]:
            return queryset
        case None:
            return queryset
        case _:
            print(nrocertificado)
            nrocertificado = int(nrocertificado[0])
            print(nrocertificado)
            if anulado:
                cert = Certificados.objects.filter(
                    nrocertificado__exact=nrocertificado, anulado__exact=1
                ).values()
            else:
                cert = Certificados.objects.filter(
                    nrocertificado__exact=nrocertificado,
                ).values()

            print("CERTIFICADOS QUERYSET ===>")
            print(cert)

            queryset = Verificaciones.objects.none()  # Initialize an empty queryset
            if cert:
                cert = cert.first()
                if model == Verificaciones:
                    queryset = Verificaciones.objects.filter(
                        idverificacion=cert["idverificacion_id"],
                        idtaller=cert["idtaller_id"],
                    )
                elif model == Certificadosasignadosportaller:
                    queryset = Certificadosasignadosportaller.objects.filter(
                        nrocertificado=cert["nrocertificado"],
                        idtaller=cert["idtaller_id"],
                    )

                print(queryset)

            return queryset


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield (start_date + timedelta(n), start_date + timedelta(n + 1))


def generate_key(adjunto):
    key = f"{adjunto.idtaller}/var/www/html/taller/uploads/{adjunto.nombre}"
    return generate_presigned_url(key)


def generate_key_certificado(certificado):
    if certificado:
        print(certificado)
        certificado = certificado[0]
        key = f"{certificado.idtaller_id}/var/www/html/taller/uploads/pdf/{certificado.nombrea4}.pdf"
        return generate_presigned_url(key)
    return None


def generate_key_from_params(idtaller, nombrea4):
    key = f"{idtaller}/var/www/html/taller/uploads/pdf/{nombrea4}.pdf"
    return generate_presigned_url(key)


def check_for_anulado(verif):
    if isinstance(verif, Verificaciones):
        try:
            cert = Certificados.objects.get(
                idverificacion_id=verif.idverificacion, idtaller_id=verif.idtaller_id
            )
            return cert.anulado == 0
        except Exception as e:
            print(e)
            return True

    return True
