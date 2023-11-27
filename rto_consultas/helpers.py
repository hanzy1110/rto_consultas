from django.db.models import Q, QuerySet, Subquery
from django.db.models import Model
from django.core.cache import cache
from datetime import timedelta, datetime
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

import hashlib
import os
import re
import tempfile
from itertools import chain
from time import perf_counter
from typing import Dict, Iterable, List, Tuple, Set, Union
from dataclasses import dataclass, field

# from silk.profiling.profiler import silk_profile
from io import BytesIO
from barcode import EAN13
from barcode.writer import SVGWriter

from rto_consultas.models import (
    CccfAdjuntoscertificados,
    CccfCertificadoexcesos,
    CccfCertificados,
    CccfEmpresas,
    CccfUsuarios,
    Certificados,
    Certificadosasignadosportaller,
    Habilitacion,
    Personas,
    Serviciohab,
    Serviciostransportehab,
    Talleres,
    Verificaciones,
    Verificacionespdf,
    Usuarios,
)
from .presigned_url import (
    generate_presigned_url,
    get_s3_client,
    upload_file_to_bucket,
    upload_fileobj_to_bucket,
)
from .logging import configure_logger

LOG_FILE = os.environ["LOG_FILE"]
logger = configure_logger(LOG_FILE)
DOCS = [(i, d) for i, d in enumerate(["", "DNI", "LC", "LE", "PAS", "CUIT"])]


@dataclass
class AuxData:
    query_fields: List[str]
    form_fields: Dict[str, Tuple[Union[str, None], Union[Model, None]]]
    parsed_names: Dict[str, str]
    ids: Dict[str, str] = field(default_factory=dict)
    attributes: Dict[str, str] = field(default_factory=dict)
    types: Dict[str, str] = field(default_factory=dict)
    fecha_field: str = "fecha"
    aux: Dict[str, str] = field(default_factory=dict)
    render_url: str = ""
    render_form: str = ""


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


def parse_license_plate_type(value):
    # Remove any non-alphanumeric characters from the input value
    # value = value[0]
    alphanumeric_only = re.sub(r"\W", "", value)
    mercosur = True

    # Format the license plate
    if len(alphanumeric_only) >= 7:
        formatted_value = re.sub(
            r"^(\w{2})(\d{3})(\w{2})$", r"\1-\2-\3", alphanumeric_only
        )
    elif len(alphanumeric_only) >= 6:
        formatted_value = re.sub(r"^(\w{3})(\d{3})$", r"\1-\2", alphanumeric_only)
        mercosur = False
    else:
        formatted_value = alphanumeric_only

    return formatted_value, mercosur


def handle_query(request, model, fecha_field="fecha"):
    query = request.GET.copy()
    sort = query.pop("sort", None)
    page = query.pop("page", None)
    _export = query.pop("_export", None)
    nrocertificado = query.pop("nrocertificado", None)
    anulado = query.pop("anulado", None)

    tipo_dni = query.pop("dni", None)
    nro_dni = query.pop("nro_dni", None)

    tipo_dni = handle_querydict(tipo_dni)
    nro_dni = handle_querydict(nro_dni)

    query.pop("csrfmiddlewaretoken", None)

    cert_init = query.pop("cert_init", None)
    cert_end = query.pop("cert_end", None)

    cert_init, cert_end = handle_cert_insert(
        query.get("idtaller", None), cert_init, cert_end
    )

    if cert_init and cert_end:
        queryset = handle_nrocertificados(cert_init, anulado, model, cert_end)
        return queryset
    else:
        queryset = handle_nrocertificados(nrocertificado, anulado, model)

    if not check_for_empty_query(query):
        queryset = handle_args(query, queryset, fecha_field=fecha_field)
    if sort:
        queryset = queryset.order_by(sort[0])

    if tipo_dni and nro_dni:
        queryset = handle_dni(queryset, tipo_dni, nro_dni, model)

    queryset = handle_anulado(queryset, anulado, model)

    return queryset


def handle_dni(queryset, tipo_dni, nro_dni, model):
    tipo_dni = next(filter(lambda t: t[0] == tipo_dni, DOCS))[1]

    logger.debug(f"TIPO DNI: {tipo_dni} || NRO DNI: {nro_dni}")
    # ASS PROTECTION
    # queryset_copy = queryset.all()
    try:
        if tipo_dni == "CUIT":
            query = Q(cuitprestserv=str(nro_dni))
            logger.debug(f"CUIT QUERY => {queryset}")

        else:
            query = Q(ptipodoc=tipo_dni, pnrodoc=nro_dni)

        return queryset.filter(query)

    except Exception as e:
        logger.error(f"ERROR WHILE PARSING REQUEST => {e}")
        raise ValueError(f"WRONG QUERY {e}")
        # return queryset_copy


def handle_cert_insert(taller_id, cert_init, cert_end):
    logger.debug(f"PARAMS TO HANDLE:, {taller_id}, {cert_init}, {cert_end}")

    if taller_id and cert_end and cert_init:
        # TODO Check bounds for c]ertificate numbers...
        taller_id = int(taller_id) if isinstance(taller_id, str) else taller_id
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

        try:
            Certificadosasignadosportaller.objects.bulk_create(certs)
            return cert_init, cert_end
        except Exception as e:
            logger.error("ERROR DURING INSERTING CERTS...")
            logger.error(e.__cause__)

    return cert_init, cert_end
    # return None, None


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


def filter_vup(s: str):
    to_replace = "VUP - "
    if to_replace in s:
        s.replace(to_replace, "")
    return s


def map_fields(data: AuxData, model: Model):
    values = {}

    for field, vals in data.form_fields.items():
        dfield, dmodel = vals
        if bool(dfield):
            dfield = vals[0]
            dmodel: Model = vals[1]

            cache_key = (
                f"unique_values_{model._meta.db_table}{model._meta.app_label}_{field}"
            )
            cached_values = cache.get(cache_key)

            if cached_values is None:
                logger.info(f"CACHE MISS => {cache_key}")
                try:
                    values_list = model.objects.values_list(field, flat=True).distinct()
                except Exception as e:
                    print(e)
                    values_list = dmodel.objects.values_list(
                        "descripcion", flat=True
                    ).distinct()

                descriptions = dmodel.objects.values_list(dfield, flat=True).distinct()
                descriptions = list(map(filter_vup, descriptions))

                vals = {v: d for v, d in zip(values_list, descriptions)}
                values[field] = vals

                cache.set(cache_key, vals)
            else:
                logger.info(f"CACHE HIT => {cached_values}")
                values[field] = cached_values

        else:
            values[field] = {0: "Falso", 1: "Verdadero"}

    return values


def handle_context(context, view):
    logger.info("Handling context!")

    # Workaround for circular import...
    context["form"] = view.form_class(view.aux_data, view.model)

    # val_dict = handle_form(view.aux_data, view.model)
    # context["form_fields"] = val_dict
    # context["descriptions"] = map_fields(view.aux_data, view.model)
    # context["parsed_fields"] = view.aux_data.parsed_names

    fields = view.model._meta.fields
    context["fields"] = fields

    context["query_fields"] = view.aux_data.query_fields
    context["ids"] = view.aux_data.ids
    context["types"] = view.aux_data.types

    context["aux"] = view.aux_data.aux

    context["render_url"] = view.aux_data.render_url
    context["render_form"] = view.aux_data.render_form

    # logger.debug(f"Context: {context}")
    return context


def get_certs(queryset):
    for q in queryset:
        logger.debug("QUERY FOR CERT ")
        yield Certificados.objects.get(
            idtaller_id__iexact=q.idtaller_id, idverificacion_id=q.idverificacion
        )


def handle_anulado(queryset, anulado, model):
    # _queryset = model.objects.all()
    # vals = {"Verdadero": 1, "Falso": 0}
    try:
        anulado = int(anulado[0])
    except:
        anulado = None

    logger.info(f"ANULADO: {anulado}")
    match anulado:
        case [""]:
            return queryset
        case None:
            return queryset
        case _:
            logger.debug(f"STARTING ANULADO QUERY...")

            logger.info(f"FILTERING FOR MODEL => {model}")
            if model == Verificaciones:
                start = perf_counter()
                queryset_b = Certificados.objects.filter(anulado=anulado).filter(
                    idtaller__in=queryset.values_list("idtaller", flat=True),
                    idverificacion__in=queryset.values_list(
                        "idverificacion", flat=True
                    ),
                )

                related_objects_in_a = queryset.filter(
                    idtaller__in=queryset_b.values_list("idtaller", flat=True),
                    idverificacion__in=queryset_b.values_list(
                        "idverificacion", flat=True
                    ),
                )

                # logger.info("EVALUATING QUERYSET TO DEBUG...")
                # list(related_objects_in_a)

                end = perf_counter()

                ellapsed_time = end - start

                logger.debug(f"TIME ELAPSED => {ellapsed_time:.6f} seconds")

                return related_objects_in_a
            else:
                return queryset.filter(anulado=anulado)


def handle_nrocertificados(
    nrocertificado_init, anulado, model, nrocertificado_end=None
):
    queryset = model.objects.all()

    match nrocertificado_init:
        case [""]:
            return queryset
        case None:
            return queryset
        case _:
            nrocertificado_init = int(nrocertificado_init[0])
            if anulado:
                cert = Certificados.objects.filter(
                    nrocertificado__exact=nrocertificado_init, anulado__exact=1
                ).values()
            else:
                logger.info("Handling multiple certs")
                match nrocertificado_end:
                    case [""]:
                        cert = Certificados.objects.filter(
                            nrocertificado__exact=nrocertificado_init,
                        ).values()
                    case None:
                        cert = Certificados.objects.filter(
                            nrocertificado__exact=nrocertificado_init,
                        ).values()
                    case _:
                        logger.info("MULTIPLE CERTS")
                        nrocertificado_end = int(nrocertificado_end[0])
                        assert nrocertificado_init < nrocertificado_end

                        cert = Certificados.objects.filter(
                            nrocertificado__range=(
                                nrocertificado_init,
                                nrocertificado_end,
                            ),
                        ).values()

            logger.debug("CERTIFICADOS QUERYSET ===>")
            logger.debug(cert)

            if cert:
                # cert = cert.first()
                if model == Verificaciones:
                    queryset = (
                        Verificaciones.objects.none()
                    )  # Initialize an empty queryset
                    for c in cert:
                        new_q = Verificaciones.objects.filter(
                            idverificacion=c["idverificacion_id"],
                            idtaller=c["idtaller_id"],
                        )
                        queryset = chain(queryset, new_q)
                    return list(queryset)

                elif model == Certificadosasignadosportaller:
                    queryset = Certificadosasignadosportaller.objects.none()
                    for c in cert:
                        new_q = Certificadosasignadosportaller.objects.filter(
                            nrocertificado=c["nrocertificado"],
                            idtaller=c["idtaller_id"],
                        )
                        queryset = chain(queryset, new_q)
                    return list(queryset)

                logger.info(queryset)

            return queryset


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield (start_date + timedelta(n), start_date + timedelta(n + 1))


def generate_key(adjunto, bucket_name=None):
    key = f"{adjunto.idtaller}/var/www/html/taller/uploads/{adjunto.nombre}"
    return generate_presigned_url(key, bucket_name=bucket_name)


def generate_key_certificado(certificado, bucket_name=None):
    if certificado:
        print(certificado)
        certificado = certificado[0]
        key = f"{certificado.idtaller_id}/var/www/html/taller/uploads/pdf/{certificado.nombrea4}.pdf"
        return generate_presigned_url(key, bucket_name=bucket_name)
    return None


def generate_cccf_key(certificado_adjunto, idtaller, bucket_name="rto-nqn-cccf"):
    if certificado_adjunto:
        key = f"{idtaller}/{certificado_adjunto.nombrearchivo}"
        return generate_presigned_url(key, bucket_name=bucket_name)
    return ""


def generate_key_from_params(idtaller, nombrea4, bucket_name=None):
    key = f"{idtaller}/var/www/html/taller/uploads/pdf/{nombrea4}.pdf"
    return generate_presigned_url(key, bucket_name=bucket_name)


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


def check_vup(nrocertificado):
    start = str(nrocertificado)[:3]
    match start:
        case "123":
            return False
        case "152":
            return True
        case _:
            return False
            # raise ValueError("Unknown pattern in NRO certificado")


def filter_vup_transporte(certs: QuerySet):
    vup_certs = len([c for c in certs if check_vup(c.nrocertificado)])
    transporte_certs = len([c for c in certs if not check_vup(c.nrocertificado)])
    return {"cant_vup": vup_certs, "cant_transporte": transporte_certs}


def build_barcode(id, fecha, dominio, cadena_id_servicio, build_image=True):
    # The idea is to create a hard-to-alter checksum that includes the number, domain, and date
    # First, format the certificate number to 2 digits
    cb_base = str(id).zfill(6)

    # Format the date and remove hyphens
    formatted_fecha = fecha.replace("-", "")
    cb_base += formatted_fecha

    # Combine the parts and add cadenaIdServicio
    cb_base = cb_base[:10] + cb_base[12:13] + cadena_id_servicio

    # Remove hyphens and convert the domain to uppercase
    patente_raw = dominio.replace("-", "").upper()

    # Combine all parts and hash using SHA1
    a_hashear = cb_base + "TANGOFANS" + patente_raw
    sha1 = hashlib.sha1(a_hashear.encode()).hexdigest()

    # Extract the first 11 characters of the hash, convert to decimal, and pad to 14 digits
    sha_nums = str(int(sha1[:11], 16)).zfill(14)[:10]
    final_barcode = cb_base + sha_nums
    # Or to an actual file:
    final_path = f"/tmp/{final_barcode}.svg"

    if build_image:
        with open(final_path, "wb") as f:
            EAN13(final_barcode, writer=SVGWriter()).write(f)

    # Return the final result
    return final_path, final_barcode


def handle_save_hab(cleaned_data, user):
    # $sql="INSERT INTO
    # habilitacion(nroCodigoBarrasHab,dominio,activo,
    # fechaHoraCreacion,fechaHoraUltModificacion,historialModificacion,
    # modeloVehiculo,usuarioDictamen,fechaHoraDictamen,razonSocialTitular,
    # NroCertificadoCCCF) VALUES

    logger.debug(f"CLEANED_DATA => {cleaned_data}")

    new_data = {}
    username = user.username

    new_data["dominio"] = cleaned_data["dominio"]
    new_data["modelovehiculo"] = cleaned_data["modelo"]
    new_data["nrocertificadocccf"] = cleaned_data["cccf"]
    new_data["razonsocialtitular"] = cleaned_data["titular"]
    new_data["usuariodictamen"] = username

    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data["fechahoradictamen"] = today
    new_data["fechahoraultmodificacion"] = today
    new_data["fechahoracreacion"] = today

    historialModificacion = f"Usuario creacion: {username} || Fecha y hora creacion: {today} || Modelo vehiculo: {cleaned_data['modelo']} || Dato titular/empresa: {cleaned_data['titular']} || "
    new_data["historialmodificacion"] = historialModificacion

    try:
        cccf = CccfCertificados.objects.get(dominio=cleaned_data["dominio"])
        cccf = cccf.nrocertificado
    except Exception as e:
        logger.warn(f"No hay CCCF => {e}")
        cccf = None

    new_data["nrocertificadocccf"] = cccf

    last_hab_id = Habilitacion.objects.latest("idhabilitacion").idhabilitacion

    servicios = cleaned_data["servicios"]

    # foreach($colServicios as $element){
    #     $sqlServicio="INSERT INTO serviciohab(idHabilitacion,idServiciosTransporteHab) VALUES
    #     (".$idUltimaHab.",".$element.");";
    #     //echo $sqlServicio;
    #     $base->query($sqlServicio);
    # }

    cadena_id_servicio = "".join([str(s).zfill(2) for s in servicios])
    _, barcode = build_barcode(
        last_hab_id + 1,
        str(new_data["fechahoradictamen"])[0:10],
        new_data["dominio"],
        cadena_id_servicio,
        False,
    )

    new_data["nrocodigobarrashab"] = barcode
    new_data["activo"] = 1
    new_data["idlocalidadvehiculo"] = 0
    new_data["marcavehiculo"] = ""

    new_data["nombretitular"] = ""
    new_data["nrodoctitular"] = 0
    new_data["tipodoctitular"] = ""
    new_data["idlocalidadtitular"] = 0
    new_data["domiciliotitular"] = ""
    new_data["apellidotitular"] = ""

    new_data["nombreconductor"] = ""
    new_data["apellidoconductor"] = ""
    new_data["domicilioconductor"] = ""
    new_data["idlocalidadconductor"] = 0
    new_data["tipopersona"] = ""
    new_data["cuittitular"] = ""
    new_data["idtiposervicio"] = 0

    logger.debug(f"NEW_DATA => {new_data}")

    new_hab = Habilitacion(**new_data)
    new_hab.save()

    logger.info(f"Habilitacion => {new_hab} SAVED!")

    servicios_transporte_habs = [
        Serviciostransportehab.objects.get(idserviciostransportehab=int(s))
        for s in servicios
    ]

    servs = [
        Serviciohab(**{"idhabilitacion": new_hab, "idserviciostransportehab": s})
        for s in servicios_transporte_habs
    ]
    Serviciohab.objects.bulk_create(servs)

    return new_hab


def handle_initial_hab(id_habilitacion, dominio):
    context = {}
    habilitacion = Habilitacion.objects.get(
        idhabilitacion=id_habilitacion, dominio=dominio
    )

    try:
        logger.debug(f"Checking usuario: {habilitacion}")
        user = User.objects.get(username=habilitacion.usuariodictamen).username
        username = f"{user.first_name} {user.lastname}"

    except Exception as e:
        logger.warning("User not found....")
        usuario = Usuarios.objects.get(usuario=habilitacion.usuariodictamen)
        username = f"{usuario.nombre} {usuario.apellido}"

    context["usuariodictamen"] = username
    if habilitacion.tipopersona in "Jj":
        context["titular"] = habilitacion.razonsocialtitular
    else:
        context[
            "titular"
        ] = f"{habilitacion.nombretitular} {habilitacion.apellidotitular}"

    servicios = Serviciohab.objects.filter(idhabilitacion=id_habilitacion)

    descripciones = [s.idserviciostransportehab.descripcion for s in servicios]

    modificado = bool(habilitacion.modificado)
    context["modificado"] = modificado

    context["descripciones"] = descripciones

    context["dominio"] = dominio

    context["modelo"] = habilitacion.modelovehiculo

    return context


def handle_querydict(value):
    match value:
        case [""]:
            return value[0]
        case None:
            return None
        case _:
            return int(value[0])


def truncate_name(value):
    return " ".join(list(value.split(" "))[:1])


def parse_name_length(value, ptype):
    match ptype:
        case "J":
            return truncate_name(value)
        case _:
            return " ".join([truncate_name(value[0]), truncate_name(value[1])])


def check_vigencia(verificacion):
    cache_key = f"certificado:{verificacion.idtaller}-{verificacion.idverificacion}"
    cert = cache.get(cache_key, None)
    if not cert:
        logger.warn(f"CERT NOT FOUND! CACHE MISS")
        cert = Certificados.objects.filter(
            idverificacion_id__exact=verificacion.idverificacion,
            idtaller_id__exact=verificacion.idtaller,
        ).values()

    vigencia = cert[0]["vigenciahasta"]

    if vigencia < datetime.date(datetime.today()):
        logger.debug("RESULT => VENCIDO!")
        return "background-color: #FF9999"
    return "background-color: #FFFFFF"


def handle_save_cccf(cleaned_data, user, cccf_files):
    logger.debug(f"CLEANED_DATA => {cleaned_data}")

    new_data = {}

    nrocertificado = cleaned_data.get("nrocertificado", None)

    new_data["nrocertificado"] = nrocertificado
    if nrocertificado:
        new_data["fechacalibracion"] = cleaned_data.get("fechacalibracion", None)
        new_data["fechavencimiento"] = cleaned_data.get("fechavencimiento", None)

        razonsocial = cleaned_data.get("razonsocial", None)
        cuit = cleaned_data.get("cuit", None)

        empresa = CccfEmpresas.objects.filter(cuit__iexact=cuit)
        if empresa:
            new_data["idempresa"] = empresa[0]
        else:
            empresa = CccfEmpresas(razonsocial=razonsocial, cuit=cuit)
            empresa.save()
            new_data["idempresa"] = empresa

        username = user.username
        new_data["usuario"] = username

        try:
            user = CccfUsuarios.objects.get(usuario=username)
            new_data["idtaller"] = user.idtaller
        except Exception as e:
            logger.warn("CCCF USER NOT FOUND")
            username = cleaned_data.get("usuario")
            user = CccfUsuarios.objects.get(usuario=username)
            new_data["idtaller"] = user.idtaller

        dominio, mercosur = parse_license_plate_type(cleaned_data.get("dominio", None))
        new_data["dominio"] = dominio
        new_data["nrointerno"] = cleaned_data.get("nrointerno", None)
        new_data["kilometraje"] = cleaned_data.get("kilometraje", None)

        new_data["tacmarca"] = cleaned_data.get("tacmarca", "")
        new_data["tacmodelo"] = cleaned_data.get("tacmodelo", "")
        new_data["tacnroserie"] = cleaned_data.get("tacnroserie", "")
        new_data["tactipo"] = cleaned_data.get("tactipo", "")

        new_data["relw"] = cleaned_data.get("relw", 0)
        new_data["constantek"] = cleaned_data.get("constantek", 0)
        new_data["rodado"] = cleaned_data.get("rodado", "")
        new_data["precinto"] = cleaned_data.get("precinto", 0)
        new_data["impresora"] = cleaned_data.get("impresora", 0)
        new_data["observaciones"] = cleaned_data["observaciones"]

        new_data["nroinforme"] = cleaned_data.get("nroinforme", 0)
        new_data["canthojas"] = cleaned_data.get("canthojas", 0)

        new_data["desconexioncantidad"] = cleaned_data.get("desconexioncantidad", None)
        new_data["desconexionhora"] = cleaned_data.get("desconexionhora", None)
        new_data["aperturaequipo"] = int(cleaned_data.get("aperturaequipo", None))
        new_data["faltainformacion"] = int(cleaned_data.get("faltainformacion", None))
        new_data["fallasdispositivo"] = int(cleaned_data.get("fallasdispositivo", None))
        new_data["retiroelementograbacion"] = int(
            cleaned_data.get("retiroelementograbacion", None)
        )

        today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_data["fechahoracarga"] = datetime.now()
        new_data["idestado"] = 1
        new_data["idestado"] = 1
        new_data["patentemercosur"] = int(mercosur)
        _, final_barcode = build_barcode(nrocertificado, today, dominio, "123")
        new_data["cb"] = final_barcode
        new_data["cbverificador"] = final_barcode

        new_cccf = CccfCertificados(**new_data)
        new_cccf.save()
        cache_key = f"excesos_{nrocertificado if nrocertificado else 0}"
        prev_data = cache.get(cache_key, [])
        try:
            for data in prev_data:
                data["idcertificado"] = new_cccf
                data.pop("nrocertificado")
                new_exceso = CccfCertificadoexcesos(**data)
                new_exceso.save()
        except Exception as e:
            logger.error(e)

        # last_cccf_id = CccfCertificados.objects.latest("idcertificado").idcertificado
        last_cccf_id = new_cccf.idcertificado

        for _file in cccf_files:
            try:
                data = {}
                data["nombrearchivo"] = _file.name
                data["idcertificado"] = last_cccf_id
                new_cccf_adjunto = CccfAdjuntoscertificados(**data)
                new_cccf_adjunto.save()
                logger.info(f"FILE => {_file.name} SAVED!")

            except Exception as e:
                logger.error(f"ERROR WHILE SAVING FILE => {_file.name}")
        return new_cccf


def handle_initial_cccf(nrocertificado, dominio):
    context = {}
    cccf = CccfCertificados.objects.get(nrocertificado=nrocertificado, dominio=dominio)

    try:
        logger.debug(f"Checking usuario: {cccf}")
        user = User.objects.get(username=cccf.usuariodictamen).username
        username = f"{user.first_name} {user.lastname}"

    except Exception as e:
        logger.warning("User not found....")
        usuario = Usuarios.objects.get(usuario=cccf.usuariodictamen)
        username = f"{usuario.nombre} {usuario.apellido}"

    context["usuariodictamen"] = username
    if cccf.tipopersona in "Jj":
        context["titular"] = cccf.razonsocialtitular
    else:
        context["titular"] = f"{cccf.nombretitular} {cccf.apellidotitular}"

    servicios = Serviciohab.objects.filter(idhabilitacion=nrocertificado)

    descripciones = [s.idserviciostransportehab.descripcion for s in servicios]

    modificado = bool(cccf.modificado)
    context["modificado"] = modificado

    context["descripciones"] = descripciones

    context["dominio"] = dominio

    context["modelo"] = cccf.modelovehiculo

    return context


def handle_upload_file(file, s3_prefix, bucket_name=None):
    # TODO Upload to S3
    s3 = get_s3_client()
    # for k, f in files.items():
    logger.debug(f"FILE NAME => {file.name}")
    logger.debug(f"FILE => {file}")
    logger.debug(f"{s3_prefix}/{file.name}")

    s3_key = f"{s3_prefix}/{file.name}"

    upload_fileobj_to_bucket(file, s3_key, s3_client=s3, bucket_name=None)

    # with tempfile.TemporaryFile() as fp:
    #     for chunk in file.chunks():
    #         fp.write(chunk)

    #     # "s3_key is the path within the bucket"
    # upload_file_to_bucket(
    #     file_path=fp.name,
    #     bucket_name=bucket_name,
    #     s3_client=s3,
    #     s3_key=s3_key,
    # )


def allow_keys(data: dict, keys: list[str]):
    return {k: data[k] for k in keys}
