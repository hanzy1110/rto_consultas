import django_tables2 as tables
from django.core.paginator import Paginator
from django.utils.html import format_html
from django.templatetags.static import static
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import timedelta

from rto_consultas_rn.models import (
    # VWVerificaciones,
    Localidades,
    Oits,
    Excepcion,
    Usuarios,
    Verificacionespdf,
    Tipovehiculo,
    Verificaciones,
    Vehiculos,
    Personas,
    Certificados,
    Certificadosasignadosportaller,
    Serviciostransporte,
)
from rto_consultas_rn.models import Estados, Tipousovehiculo, Talleres
from rto_consultas.helpers import (
    LOG_FILE,
    AuxData,
    map_fields,
    generate_key_from_params,
    check_vigencia,
    convert_date,
    parse_name_length,
)
from rto_consultas.logging import configure_logger

logger = configure_logger(LOG_FILE)

# from silk.profiling.profiler import silk_profile
from django.core.cache import cache

VALS = {1: "Verdadero", 0: "Falso"}
VALS_ANULADO = {1: "anulado", 0: "vigente"}
DESCRIPTIONS = {
    1: "Particular",
    2: "Transporte de Carga",
    3: "Transporte Pasajeros",
    4: "Transporte Municipal",
}
ESTADO_CERTIFICADO = {
    1: "Aprobado",
    2: "Rechazado",
    3: "Aprobado Condicional",
    4: "Reverificado",
    5: "Vencido",
}


class ImageColumn(tables.Column):
    def render(self, record):
        cache_key = f"{record.idverificacion}"

        cert = cache.get(cache_key, None)

        logger.info("CACHE HIT IMAGE COLUMN")

        if not cert:
            cert = Certificados.objects.filter(
                idverificacion_id__exact=record.idverificacion,
                idtaller_id__exact=record.idtaller,
            ).values()
            logger.info("CACHE MISS IMAGE COLUMN")

            cert = cert[0]

        key = VALS_ANULADO[cert["anulado"]]
        # Use the static template tag to generate the image URL
        image_url = static(f"img/small-logos/{key}.png")
        # Return the HTML with the correct image URL
        return format_html('<img src="{}" />', image_url)
        # return format_html('<img src="{% static img/small-logos/{}.png}" />', key)
        # return format_html('<img src="{% static img/small-logos/{}.png %}" />', key)
        # return format_html('<img src="img/small-logos/{}.png" />', key)


class ImageColumnAprobado(tables.Column):
    def render(self, record):
        key = VALS_ANULADO.get(record.aprobado, "anulado")
        # Use the static template tag to generate the image URL
        image_url = static(f"img/small-logos/{key}.png")
        # Return the HTML with the correct image URL
        return format_html('<img src="{}" />', image_url)


class FileColumnHabs(tables.FileColumn):
    def render(self, value, record):
        url = self.get_url(value, record)

        idhabilitacion = record.idhabilitacion

        url = reverse(
            "pdfhabilitacion",
            args=[idhabilitacion],
        )

        logger.debug(f"URL => {url}")
        cache_key = f"{record.idhabilitacion}"
        cached_cert = cache.get(cache_key)

        image_url = static(f"img/small-logos/pdf-flat.png")

        if url:
            atag = format_html(
                '<a href="{}" target="_blank"><img src="{}" alt="Image"></a>',
                url,
                image_url,
            )

        else:
            img_not_found = static(f"img/small-logos/cert_no_encontrado2.png")
            atag = format_html('<img src="{}" alt="Image">', img_not_found)

        logger.debug(f"atag => {atag}")
        if cached_cert:
            # nro_cert = Certificados.objects.get(idverificacion_id=record.idverificacion)
            logger.info("CACHE HIT")
            return atag
            # return str(nro_cert)
        else:
            # nro_cert = Certificados.objects.get(idverificacion_id=record.idverificacion)
            logger.info("CACHE MISS")
            return atag


class CustomFileColumn(tables.FileColumn):
    def get_url(self, value, record):
        certificado = Verificacionespdf.objects.filter(
            idtaller_id__exact=record.idtaller,
            idverificacion_id__exact=record.idverificacion,
        )
        if certificado:
            certificado = certificado[0].values()

            cache_key = f"{certificado['idverificacion']}-{certificado['idtaller']}"
            cache.set(cache_key, certificado)
            url = generate_key_from_params(
                certificado.idtaller_id,
                certificado.nombrea4,
                bucket_name="rto-rn-files",
            )
            return url
        return value

    def render(self, value, record):
        url = self.get_url(value, record)
        logger.debug(f"URL => {url}")
        cache_key = f"{record.idverificacion}"
        cached_cert = cache.get(cache_key)

        image_url = static(f"img/small-logos/pdf-flat.png")

        if url:
            atag = format_html(
                '<a href="{}" target="_blank"><img src="{}" alt="Image"></a>',
                url,
                image_url,
            )

        else:
            img_not_found = static(f"img/small-logos/cert_no_encontrado2.png")
            atag = format_html('<img src="{}" alt="Image">', img_not_found)

        logger.debug(f"atag => {atag}")
        if cached_cert:
            # nro_cert = Certificados.objects.get(idverificacion_id=record.idverificacion)
            logger.info("CACHE HIT")
            return atag
            # return str(nro_cert)
        else:
            # nro_cert = Certificados.objects.get(idverificacion_id=record.idverificacion)
            logger.info("CACHE MISS")
            return atag


class VerificacionesTables(tables.Table):
    dominiovehiculo = tables.Column(verbose_name="Dominio")
    certificado = tables.Column(
        verbose_name="Nro. Certificado",
        empty_values=(),
    )
    fecha = tables.DateColumn(orderable=True, verbose_name="Emision", format="d/m/Y")
    ver_verificacion = tables.Column(
        verbose_name="Consulta",
        linkify=(
            "ver_verificacion_rn",
            {
                "idverificacion": tables.A("idverificacion"),
                "idtaller": tables.A("idtaller__idtaller"),
            },
        ),
        empty_values=(),
        attrs={"th": {"colspan": "4"}},
    )  # (viewname, kwargs)
    ver_certificado = CustomFileColumn(
        verbose_name="Certificado", empty_values=(), attrs={"th": {"hidden": True}}
    )  # (viewname, kwargs)
    titular = tables.Column(empty_values=())
    anulado = ImageColumn(
        empty_values=(), verbose_name="Estado", attrs={"th": {"hidden": True}}
    )
    vigencia = tables.Column(empty_values=())
    idtaller = tables.Column(empty_values=(), verbose_name="Planta")
    idestado = tables.Column(empty_values=(), verbose_name="Calificación")
    idtipouso = tables.Column(empty_values=(), verbose_name="Tipo de Uso")
    aux_data = AuxData(
        query_fields=[],
        form_fields={
            "idestado": ("descripcion", Estados),
            "idtipouso": ("descripcion", Tipousovehiculo),
            "idtipovehiculo": ("descripcion", Tipovehiculo),
            "idtaller": ("nombre", Talleres),
        },
        parsed_names={"name": "name"},
    )
    auditado = ImageColumn(
        empty_values=(), verbose_name="", attrs={"th": {"hidden": True}}
    )

    class Meta:
        model = Verificaciones
        row_attrs = {"style": lambda record: check_vigencia(record, sender="RN")}
        orderable = False
        fields = (
            "dominiovehiculo",
            "certificado",
            "fecha",
            "vigencia",
            "idestado",
            "idtipouso",
            # "titular",
            "ver_verificacion",
            "ver_certificado",
            "anulado",
            "auditado",
            "idtaller",
        )
        extra_columns = ("certificado",)
        template_name = "tables/htmx_table_RN.html"

    def render_ver_verificacion(self, record):
        image_url = static(f"img/small-logos/ver.png")
        return format_html('<img src="{}" />', image_url)

    def render_idestado(self, value):
        try:
            return ESTADO_CERTIFICADO[value.idestado]
        except Exception as e:
            print(e)
            return "Unknown!"

    def render_idtipovehiculo(self, record):
        try:
            idtipovehiculo = record.idtipovehiculo
            return Tipovehiculo.objects.get(
                idtipovehiculo__exact=idtipovehiculo
            ).descripcion
        except Exception as e:
            print(e)
            return "N/E"

    def render_idtipouso(self, value):
        try:
            return DESCRIPTIONS[value]

        except Exception as e:
            print(e)
            return "Unknown!"

    def render_auditado(self, record):
        image_url = static(f"img/small-logos/auditoria.png")
        return format_html('<img src="{}" width="25px"/>', image_url)

    def render_vigencia(self, record):
        cert = Certificados.objects.filter(
            idverificacion_id__exact=record.idverificacion,
            idtaller_id__exact=record.idtaller,
        ).values()
        return convert_date(cert[0]["vigenciahasta"])

    def render_certificado(self, record):
        query = self.Meta.model.get_nro_certificado(record)
        return query

    def render_idtaller(self, value):
        return value.nombre

    def render_titular(self, record):
        persona = record.codigotitular

        match persona.tipopersona:
            case "J":
                return parse_name_length(persona.razonsocial, "J")
            case _:
                return parse_name_length([persona.nombre, persona.apellido], "P")

    def paginate(
        self, paginator_class=Paginator, per_page=None, page=1, *args, **kwargs
    ):
        per_page = per_page or self._meta.per_page
        self.paginator = paginator_class(self.rows, per_page, *args, **kwargs)
        self.page = self.paginator.page(page)

        return self


class VehiculosTable(tables.Table):
    aux_data = AuxData(
        query_fields=[],
        form_fields={"idtipouso": ("descripcion", Tipousovehiculo)},
        parsed_names={"name": "name"},
    )

    class Meta:
        template_name = "tables/htmx_table_RN.html"
        model = Vehiculos
        fields = {"dominio", "idtipouso", "marca"}

    def render_idtipouso(self, value):
        try:
            descriptions = map_fields(self.aux_data, self.Meta.model)
            return descriptions["idtipouso"][value.idtipouso]

        except Exception as e:
            print(e)
            return "Unknown!"

    def paginate(
        self, paginator_class=Paginator, per_page=None, page=1, *args, **kwargs
    ):
        per_page = per_page or self._meta.per_page
        self.paginator = paginator_class(self.rows, per_page, *args, **kwargs)
        self.page = self.paginator.page(page)

        return self


class CertificadosTable(tables.Table):
    aux_data = AuxData(
        query_fields=[],
        form_fields={"idtaller": ("nombre", Talleres)},
        parsed_names={"name": "name"},
    )

    class Meta:
        template_name = "tables/htmx_table_RN.html"
        model = Certificados
        fields = {"nrocertificado", "idtaller", "fecha", "anulado"}

    def render_idtaller(self, value):
        return value.nombre

    def paginate(
        self, paginator_class=Paginator, per_page=None, page=1, *args, **kwargs
    ):
        per_page = per_page or self._meta.per_page
        self.paginator = paginator_class(self.rows, per_page, *args, **kwargs)
        self.page = self.paginator.page(page)

        return self


class CertificadosAssignTable(tables.Table):
    # aux_data = AuxData(
    # 	query_fields=[],
    # 	form_fields={ "idtaller":("nombre", Talleres) },
    # 	parsed_names={"name":"name"}
    # )
    nrocertificado = tables.Column(verbose_name="Nro. Certificado")
    idtaller = tables.Column(verbose_name="Planta")
    disponible = tables.Column(verbose_name="Disponible")
    replicado = tables.Column(verbose_name="Replicado")
    fechacarga = tables.Column(verbose_name="Fecha Carga")

    class Meta:
        template_name = "tables/htmx_table_RN.html"
        model = Certificadosasignadosportaller
        query_fields = {"nrocertificado", "idtaller", "disponible", "replicado"}

    def paginate(
        self, paginator_class=Paginator, per_page=None, page=1, *args, **kwargs
    ):
        per_page = per_page or self._meta.per_page
        self.paginator = paginator_class(self.rows, per_page, *args, **kwargs)
        self.page = self.paginator.page(page)

        return self


class CertificadosTablesResumen(tables.Table):
    Aprobado = tables.Column(empty_values=(), orderable=False)
    RechazadoLeveModerado = tables.Column(empty_values=(), orderable=False)
    RechazadoGrave = tables.Column(empty_values=(), orderable=False)
    # certificado = tables.Column(empty_values=(), orderable=False)
    aux_data = AuxData(
        query_fields=[],
        form_fields={
            "idestado": ("descripcion", Estados),
            "idtipouso": ("descripcion", Tipousovehiculo),
            "idtaller": ("nombre", Talleres),
        },
        parsed_names={"name": "name"},
    )

    class Meta:
        template_name = "tables/htmx_table_RN.html"
        model = Certificados
        fields = (
            "nrocertificado",
            "fecha",
            "idtaller",
            "dominiovehiculo",
            "Aprobado",
            "RechazadoLeveModerado",
            "RechazadoGrave",
        )
        extra_columns = ("certificado",)

    def render_idtipouso(self, value):
        try:
            descriptions = map_fields(self.aux_data, self.Meta.model)
            return descriptions["idtipouso"][value]

        except Exception as e:
            print(e)
            return "Unknown!"

    def render_idtaller(self, value):
        return value.nombre

    def value_RechazadoGrave(self, record):
        if record.idestado == 2:
            return 1
        return 0

    def value_RechazadoLeveModerado(self, record):
        if record.idestado == 3:
            return 1
        return 0

    def value_Aprobado(self, record):
        if record.idestado == 1:
            return 1
        return 0

    def render_RechazadoGrave(self, record):
        if record.idestado == 2:
            return 1
        return 0

    def render_RechazadoLeveModerado(self, record):
        if record.idestado == 3:
            return 1
        return 0

    def render_Aprobado(self, record):
        if record.idestado == 1:
            return 1
        return 0

    def paginate(
        self, paginator_class=Paginator, per_page=None, page=1, *args, **kwargs
    ):
        per_page = per_page or self._meta.per_page
        self.paginator = paginator_class(self.rows, per_page, *args, **kwargs)
        self.page = self.paginator.page(page)

        return self


class VerificacionesAnuales(tables.Table):
    year = tables.Column()
    cant_verificaciones = tables.Column()
    cant_aprobados = tables.Column()
    cant_rechazados = tables.Column()
    cant_aprobados_condicionales = tables.Column()


class ObleasPorTallerTable(tables.Table):
    taller = tables.Column(verbose_name="Planta")
    cant_vup = tables.Column(verbose_name="ANSV")
    cant_transporte = tables.Column(verbose_name="DPT")

    class Meta:
        template_name = "tables/htmx_table_RN.html"


class ResumenTransporteTable(tables.Table):
    certificado = tables.Column(
        orderable=False,
        empty_values=(),
    )
    fecha = tables.DateColumn(format="d/m/Y")
    titular = tables.Column(orderable=False, empty_values=())
    marca = tables.Column(orderable=False, empty_values=())
    modelo = tables.Column(orderable=False, empty_values=())
    anio_fab = tables.Column(orderable=False, empty_values=())
    tipo_servicio = tables.Column(orderable=False, empty_values=())
    aux_data = AuxData(
        query_fields=[],
        form_fields={
            "idestado": ("descripcion", Estados),
            "idtipouso": ("descripcion", Tipousovehiculo),
            "idtipovehiculo": ("descripcion", Tipovehiculo),
            "idtaller": ("nombre", Talleres),
        },
        parsed_names={"name": "name"},
    )

    class Meta:
        template_name = "tables/htmx_table_RN.html"
        model = Verificaciones
        fields = (
            "certificado",
            "localidad",
            "fecha",
            "idtaller",
            "titular",
            "dominiovehiculo",
            "marca",
            "modelo",
            "anio_fab",
            "tipo_servicio",
            # PONER TIPO CARGA ACA EN VEZ DE SERVICIO PARA TRANSPORTE CARGA
            "idtipovehiculo",
            "idestado",
        )
        extra_columns = ("certificado",)

    def render_idestado(self, value):
        try:
            descriptions = map_fields(self.aux_data, self.Meta.model)
            return descriptions["idestado"][value.idestado]
            # return value.descripcion
        except Exception as e:
            print(e)
            return "Unknown!"

    def render_idtipovehiculo(self, record):
        try:
            descriptions = map_fields(self.aux_data, self.Meta.model)
            return descriptions["idtipovehiculo"][record.idtipovehiculo]
            # return value.descripcion
        except Exception as e:
            print(e)
            return "Unknown!"

    def render_idtipouso(self, value):
        try:
            descriptions = map_fields(self.aux_data, self.Meta.model)
            return descriptions["idtipouso"][value]

        except Exception as e:
            print(e)
            return "Unknown!"

    def render_certificado(self, record):
        query = self.Meta.model.get_nro_certificado(record)
        return query

    def render_idtaller(self, value):
        return value.nombre

    def render_titular(self, record):
        persona = record.codigotitular
        match persona.tipopersona:
            case "J":
                return persona.razonsocial
            case _:
                return f"{persona.nombre} {persona.apellido}"

    def render_marca(self, record):
        return record.vmarca

    def render_modelo(self, record):
        return record.vmodelo

    def render_anio_fab(self, record):
        return record.vanio

    def render_tipo_servicio(self, record):
        try:
            return Serviciostransporte.objects.get(
                idtiposervicio__exact=record.idtiposervicio
            )
        except Exception as e:
            return "N/A"

    def render_localidad(self, record):
        try:
            localidad = Localidades.objects.get(
                idlocalidad__exact=record.pidlocalidad
            ).descripcion
            return localidad if localidad else "N/E"
        except:
            return "N/E"

    def paginate(
        self, paginator_class=Paginator, per_page=None, page=1, *args, **kwargs
    ):
        per_page = per_page or self._meta.per_page
        self.paginator = paginator_class(self.rows, per_page, *args, **kwargs)
        self.page = self.paginator.page(page)

        return self


class ResumenTransporteCargaTable(tables.Table):
    certificado = tables.Column(
        orderable=False,
        empty_values=(),
    )
    fecha = tables.DateColumn(format="d/m/Y")
    titular = tables.Column(orderable=False, empty_values=())
    marca = tables.Column(orderable=False, empty_values=())
    modelo = tables.Column(orderable=False, empty_values=())
    anio_fab = tables.Column(orderable=False, empty_values=())
    tipo_carga = tables.Column(orderable=False, empty_values=())
    localidad = tables.Column(orderable=False, empty_values=())
    aux_data = AuxData(
        query_fields=[],
        form_fields={
            "idestado": ("descripcion", Estados),
            "idtipouso": ("descripcion", Tipousovehiculo),
            "idtipovehiculo": ("descripcion", Tipovehiculo),
            "idtaller": ("nombre", Talleres),
        },
        parsed_names={"name": "name"},
    )

    class Meta:
        template_name = "tables/htmx_table_RN.html"
        model = Verificaciones
        fields = (
            "certificado",
            "localidad",
            "fecha",
            "idtaller",
            "titular",
            "dominiovehiculo",
            "marca",
            "modelo",
            "anio_fab",
            "tipo_carga",
            "idtipovehiculo",
            "idestado",
        )
        extra_columns = ("certificado",)

    def render_idestado(self, value):
        try:
            descriptions = map_fields(self.aux_data, self.Meta.model)
            return descriptions["idestado"][value.idestado]
            # return value.descripcion
        except Exception as e:
            print(e)
            return "Unknown!"

    def render_idtipovehiculo(self, record):
        try:
            descriptions = map_fields(self.aux_data, self.Meta.model)
            return descriptions["idtipovehiculo"][record.idtipovehiculo]
            # return value.descripcion
        except Exception as e:
            print(e)
            return "Unknown!"

    def render_idtipouso(self, value):
        try:
            descriptions = map_fields(self.aux_data, self.Meta.model)
            return descriptions["idtipouso"][value]

        except Exception as e:
            print(e)
            return "Unknown!"

    def render_certificado(self, record):
        query = self.Meta.model.get_nro_certificado(record)
        return query

    def render_idtaller(self, value):
        return value.nombre

    def render_titular(self, record):
        persona = record.codigotitular
        match persona.tipopersona:
            case "J":
                return persona.razonsocial
            case _:
                return f"{persona.nombre} {persona.apellido}"

    def render_marca(self, record):
        return record.vmarca

    def render_modelo(self, record):
        return record.vmodelo

    def render_anio_fab(self, record):
        return record.vanio

    def value_tipo_carga(self, record):
        try:
            tipo_carga = Vehiculos.objects.get(
                dominio__exact=record.dominiovehiculo
            ).tipocarga
            return tipo_carga if tipo_carga else "No Especificado"
        except:
            return "N/A"

    def value_localidad(self, record):
        try:
            localidad = Localidades.objects.get(
                idlocalidad__exact=record.pidlocalidad
            ).descripcion
            return localidad if localidad else "N/E"
        except:
            return "N/E"

    def render_tipo_carga(self, record):
        try:
            tipo_carga = Vehiculos.objects.get(
                dominio__exact=record.dominiovehiculo
            ).tipocarga
            return tipo_carga if tipo_carga else "No Especificado"
        except:
            return "N/A"

    def render_localidad(self, record):
        try:
            localidad = Localidades.objects.get(
                idlocalidad__exact=record.pidlocalidad
            ).descripcion
            return localidad if localidad else "N/E"
        except:
            return "N/E"

    def paginate(
        self, paginator_class=Paginator, per_page=None, page=1, *args, **kwargs
    ):
        per_page = per_page or self._meta.per_page
        self.paginator = paginator_class(self.rows, per_page, *args, **kwargs)
        self.page = self.paginator.page(page)

        return self


class OitsTable_RN(tables.Table):
    aux_data = AuxData(
        query_fields=[],
        form_fields={},
        parsed_names={"name": "name"},
    )

    # vista_previa = tables.Column(
    #     verbose_name="Consulta",
    #     linkify=(
    #         "ver_habilitacion",
    #         {
    #             "idhabilitacion": tables.A("idhabilitacion"),
    #             "dominio": tables.A("dominio"),
    #         },
    #     ),
    #     orderable=False,
    #     empty_values=(),
    #     # attrs={"th": {"colspan": "4"}},
    # )  # (viewname, kwargs)

    numero = tables.Column(verbose_name="Nro. Orden Inspección")
    dominio = tables.Column(verbose_name="Dominio")
    # razonsocial = tables.Column(verbose_name="Titular")
    fecha = tables.Column(verbose_name="Fecha Desde")
    vista_previa = tables.Column(verbose_name="Vista Previa")

    vigencia = tables.Column(
        verbose_name="Fecha Hasta", orderable=False, empty_values=()
    )

    class Meta:
        template_name = "tables/htmx_table.html"
        model = Oits
        fields = [
            "numero",
            "dominio",
            # "razonsocial",
            "fecha",
            "vigencia",
            # HYPERLINKS:
            # "vista_previa",
        ]

    # def render_vista_previa(self, record):
    #     image_url = static(f"img/small-logos/lupa.png")
    #     return format_html('<img src="{}" width="25px"/>', image_url)

    def render_vigencia(self, record):
        fecha = record.fecha
        logger.debug(f"FECHA => {fecha}")
        vigencia = fecha + timedelta(days=15.0)
        return vigencia

    def paginate(
        self, paginator_class=Paginator, per_page=None, page=1, *args, **kwargs
    ):
        per_page = per_page or self._meta.per_page
        self.paginator = paginator_class(self.rows, per_page, *args, **kwargs)
        self.page = self.paginator.page(page)

        return self


class ProrrogasTable_RN(tables.Table):
    aux_data = AuxData(
        query_fields=[],
        form_fields={},
        parsed_names={"name": "name"},
    )

    dominio = tables.Column(verbose_name="Dominio")
    fechahoracreacion = tables.Column(verbose_name="Fecha Hora Creación")
    fundamentacionpeticion = tables.Column(verbose_name="Fundamentación Petición")
    fundamentaciondictamen = tables.Column(verbose_name="Fundamentación Dictamen")
    idtaller = tables.Column(verbose_name="Planta", orderable=False, empty_values=())
    # aprobado = ImageColumnAprobado(
    #     empty_values=(), verbose_name="Estado", attrs={"th": {"hidden": True}}
    # )

    class Meta:
        template_name = "tables/htmx_table.html"
        model = Excepcion
        fields = [
            "dominio",
            "nrocertificado",
            "fechahoracreacion",
            "idtaller",
            "fundamentacionpeticion",
            "fundamentaciondictamen",
            # "aprobado"
            # HYPERLINKS:
            # "vista_previa",
        ]

    # def render_vista_previa(self, record):
    #     image_url = static(f"img/small-logos/lupa.png")
    #     return format_html('<img src="{}" width="25px"/>', image_url)

    def render_idtaller(self, value):
        try:
            taller = Talleres.objects.get(idtaller=value)
            return taller.nombre
        except Exception as e:
            logger.warn(e)
            return "UNK"

    def paginate(
        self, paginator_class=Paginator, per_page=None, page=1, *args, **kwargs
    ):
        per_page = per_page or self._meta.per_page
        self.paginator = paginator_class(self.rows, per_page, *args, **kwargs)
        self.page = self.paginator.page(page)

        return self


class ExcepcionesTable_RN(tables.Table):
    aux_data = AuxData(
        query_fields=[],
        form_fields={},
        parsed_names={"name": "name"},
    )

    dominio = tables.Column(verbose_name="Dominio")
    titular = tables.Column(orderable=False, empty_values=())
    fecha = tables.Column(verbose_name="Fecha Desde")
    modelovehiculo = tables.Column(verbose_name="Modelo Vehiculo")
    marcavehiculo = tables.Column(verbose_name="Marca Vehiculo")
    idtaller = tables.Column(verbose_name="Planta", orderable=False, empty_values=())
    # aprobado = ImageColumnAprobado(
    #     empty_values=(), verbose_name="Estado", attrs={"th": {"hidden": True}}
    # )

    class Meta:
        template_name = "tables/htmx_table.html"
        model = Excepcion
        fields = [
            "dominio",
            "fecha",
            "marcavehiculo",
            "modelovehiculo",
            "titular",
            "idtaller",
            # "aprobado"
            # HYPERLINKS:
            # "vista_previa",
        ]

    # def render_vista_previa(self, record):
    #     image_url = static(f"img/small-logos/lupa.png")
    #     return format_html('<img src="{}" width="25px"/>', image_url)

    def render_idtaller(self, value):
        try:
            taller = Talleres.objects.get(idtaller=value)
            return taller.nombre
        except Exception as e:
            logger.warn(e)
            return "UNK"

    def render_titular(self, record):
        if record.tipopersona in "Jj":
            return f"{record.razonsocialtitular}"
        return f"{record.nombretitular} {record.apellidotitular}"

    def paginate(
        self, paginator_class=Paginator, per_page=None, page=1, *args, **kwargs
    ):
        per_page = per_page or self._meta.per_page
        self.paginator = paginator_class(self.rows, per_page, *args, **kwargs)
        self.page = self.paginator.page(page)

        return self


class ObleasPorTallerTable(tables.Table):
    taller = tables.Column(verbose_name="Planta")
    cant_vup = tables.Column(verbose_name="ANSV")
    cant_transporte = tables.Column(verbose_name="DPT")

    class Meta:
        template_name = "tables/htmx_table.html"
