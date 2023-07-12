from django.db.models import Q, QuerySet
from django.db.models import Model


import re
from typing import Dict, List, Tuple, Set, Union
from dataclasses import dataclass, field

from rto_consultas.models import Certificados, Verificaciones


@dataclass
class AuxData:
    query_fields: List[str]
    form_fields: Dict[str, Tuple[Union[str, None], Union[Model, None]]]
    parsed_names: Dict[str, str]
    ids: Dict[str, str] = field(default_factory=dict)
    types: Dict[str, str] = field(default_factory=dict)
    fecha_field:str = "fecha"


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
        return Q(**{f"{fecha_field}__range":(date_from, date_to)})
    if date_from and not date_to:
        return Q(**{f"{fecha_field}__gte":date_from})


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
    nrocertificado = query.pop("nrocertificado", None)

    queryset = handle_nrocertificado(nrocertificado, model)
    if query:
        queryset = handle_args(query, queryset, fecha_field=fecha_field)
    if sort:
        queryset = queryset.order_by(sort[0])
    return queryset


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

            try:
                val = model.objects.values_list(field, flat=True).distinct()
            except Exception as e:
                print(e)
                val = dmodel.objects.values_list("descripcion", flat=True).distinct()

            descriptions = dmodel.objects.values_list(dfield, flat=True).distinct()
            values[field] = {v: d for v, d in zip(val, descriptions)}
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
    return context

def handle_nrocertificado(nrocertificado, model):

    queryset = model.objects.all()

    match nrocertificado:
        case ['']:
            return queryset
        case None:
            return queryset
        case _:
            print(nrocertificado)
            nrocertificado = int(nrocertificado[0])
            print(nrocertificado)
            cert = Certificados.objects.filter(nrocertificado__exact=nrocertificado)
            print("CERTIFICADOS QUERYSET ===>")
            # print(cert.first().idverificacion)
            # print(cert.first().taller)

            queryset = Verificaciones.objects.none()  # Initialize an empty queryset
            if cert.exists():
                print("DATOS CERTIFICADOS ===>")
                for c in cert:
                    print(c.idverificacion)
                    print(c.taller)

                idverificacion = cert.first().idverificacion
                idtaller = cert.first().taller
                queryset = (Verificaciones.objects
                            .filter(idverificacion=idverificacion
                                    ,taller=idtaller))
                print(queryset)

            return queryset
