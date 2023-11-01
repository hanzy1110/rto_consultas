import django_tables2 as tables
from django.core.paginator import Paginator
from django.utils.html import format_html
from django.templatetags.static import static
from django.contrib.auth.models import User
from django.urls import reverse

from .models import (
    # VWVerificaciones,
    Localidades,
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
from .models import Estados, Tipousovehiculo, Talleres
from rto_consultas.helpers import (
    LOG_FILE,
    AuxData,
    map_fields,
    generate_key_from_params,
    convert_date,
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
        cache_key = f"certificado:{record.idtaller}-{record.idverificacion}"

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


class FileColumnHabs(tables.FileColumn):
    def render(self, value, record):
        url = self.get_url(value, record)

        idhabilitacion = record.idhabilitacion

        url = reverse(
            "pdfhabilitacion",
            args=[idhabilitacion],
        )

        logger.debug(f"URL => {url}")
        cache_key = f"habilitacion:{record.idhabilitacion}"
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
            certificado = certificado[0]

            cache_key = (
                f"certificado:{certificado.idtaller_id}-{certificado.idverificacion_id}"
            )
            cache.set(cache_key, certificado)
            url = generate_key_from_params(
                certificado.idtaller_id, certificado.nombrea4
            )
            return url
        return value

    def render(self, value, record):
        url = self.get_url(value, record)
        logger.debug(f"URL => {url}")
        cache_key = f"certificado:{record.idtaller_id}-{record.idverificacion}"
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
        verbose_name="Verificación",
        linkify=(
            "ver_verificacion",
            {
                "idverificacion": tables.A("idverificacion"),
                "idtaller": tables.A("idtaller__idtaller"),
            },
        ),
        empty_values=(),
    )  # (viewname, kwargs)
    ver_certificado = CustomFileColumn(
        verbose_name="Certificado",
        empty_values=(),
    )  # (viewname, kwargs)
    titular = tables.Column(empty_values=())
    anulado = ImageColumn(empty_values=(), verbose_name="Estado")
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

    class Meta:
        model = Verificaciones
        orderable = False
        fields = (
            "dominiovehiculo",
            "certificado",
            "fecha",
            "vigencia",
            "idestado",
            "idtipouso",
            "titular",
            "ver_verificacion",
            "ver_certificado",
            # "idtipovehiculo",
            "idtaller",
            "anulado",
        )
        extra_columns = ("certificado",)
        template_name = "tables/htmx_table.html"

    def render_ver_verificacion(self, record):
        image_url = static(f"img/small-logos/ver.png")
        return format_html('<img src="{}" />', image_url)

    # def render_ver_certificado(self, record, value):
    #     cache_key = f"certificado:{record.idtaller_id}-{record.idverificacion}"
    #     cached_cert = cache.get(cache_key)

    #     image_url = static(f"img/small-logos/printer.png")
    #     img_tag = format_html('<img src="{}" />', image_url)
    #     if cached_cert:
    #         # nro_cert = Certificados.objects.get(idverificacion_id=record.idverificacion)
    #         return img_tag
    #         # return str(nro_cert)
    #     else:
    #         # nro_cert = Certificados.objects.get(idverificacion_id=record.idverificacion)
    #         return img_tag
    #         # return str(nro_cert)
    # return "No disponible"

    def render_idestado(self, value):
        try:
            # descriptions = map_fields(self.aux_data, self.Meta.model)
            return ESTADO_CERTIFICADO[value.idestado]
            # return value.descripcion
        except Exception as e:
            print(e)
            return "Unknown!"

    def render_idtipovehiculo(self, record):
        try:
            # descriptions = map_fields(self.aux_data, self.Meta.model)
            # return descriptions["idtipovehiculo"][record.idtipovehiculo]
            # return value.descripcion
            idtipovehiculo = record.idtipovehiculo
            return Tipovehiculo.objects.get(
                idtipovehiculo__exact=idtipovehiculo
            ).descripcion
        except Exception as e:
            print(e)
            return "N/E"

    # def render_anulado(self, record):
    #     cert = Certificados.objects.filter(
    #         idverificacion_id__exact=record.idverificacion,
    #         idtaller_id__exact=record.idtaller,
    #     ).values()
    #     return vals_anulado[cert[0]["anulado"]]

    def render_idtipouso(self, value):
        try:
            # descriptions = map_fields(self.aux_data, self.Meta.model)
            # logger.debug(f"DESCRIPTIONS FROM IDTIPO USO=> {descriptions}")
            # logger.debug(f"VALUE => {value}")

            return DESCRIPTIONS[value]

        except Exception as e:
            print(e)
            return "Unknown!"

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
                return persona.razonsocial
            case _:
                return f"{persona.nombre} {persona.apellido}"

    def paginate(
        self, paginator_class=Paginator, per_page=None, page=1, *args, **kwargs
    ):
        per_page = per_page or self._meta.per_page
        self.paginator = paginator_class(self.rows, per_page, *args, **kwargs)
        self.page = self.paginator.page(page)

        return self


class HabilitacionesTable(tables.Table):
    aux_data = AuxData(
        query_fields=[],
        form_fields={},
        parsed_names={"name": "name"},
    )

    vista_previa = tables.Column(
        verbose_name="Vista Previa",
        linkify=(
            "ver_habilitacion",
            {
                "idhabilitacion": tables.A("idhabilitacion"),
                "dominio": tables.A("dominio"),
            },
        ),
        orderable=False,
        empty_values=(),
    )  # (viewname, kwargs)

    nrocodigobarrashab = tables.Column(verbose_name="Nro. Orden Inspección")
    dominio = tables.Column(verbose_name="Dominio")
    titular = tables.Column(verbose_name="Titular")
    fechahoracreacion = tables.Column(verbose_name="Fecha y Hora Creación")
    usuariodictamen = tables.Column(verbose_name="Emitido Por")
    modificado = tables.Column(verbose_name="Modificado")

    # imprimir = CustomFileColumn(
    #     verbose_name="Habilitacion",
    #     orderable=False,
    #     empty_values=(),
    # )  # (viewname, kwargs)
    imprimir = FileColumnHabs(verbose_name="Imprimir", orderable=False, empty_values=())
    modificar = tables.Column(verbose_name="Modificado", default="No")

    class Meta:
        template_name = "tables/htmx_table.html"
        model = Habilitacion
        fields = [
            "nrocodigobarrashab",
            "dominio",
            "titular",
            "fechahoracreacion",
            "usuariodictamen",
            "modificado",
            # HYPERLINKS:
            "vista_previa",
            "modificar",
            "dar_de_baja",
            "imprimir",
        ]

    def render_vista_previa(self, record):
        image_url = static(f"img/small-logos/ver.png")
        return format_html('<img src="{}" />', image_url)

    def render_usuariodictamen(self, record):
        try:
            logger.debug(f"Checking usuario: {record}")
            user = User.objects.get(username=record.usuariodictamen)
            username = f"{user.first_name} {user.last_name}"

        except Exception as e:
            logger.warning("User not found....")
            usuario = Usuarios.objects.get(usuario=record.usuariodictamen)
            username = f"{usuario.nombre} {usuario.apellido}"

        return username

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
        template_name = "tables/htmx_table.html"
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
        template_name = "tables/htmx_table.html"
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

    class Meta:
        template_name = "tables/htmx_table.html"
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
        template_name = "tables/htmx_table.html"
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
        template_name = "tables/htmx_table.html"


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
        template_name = "tables/htmx_table.html"
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
        template_name = "tables/htmx_table.html"
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


class ConsultaDPTTable(tables.Table):
    Dominio = tables.Column(orderable=False, empty_values=())
    DominioProv = tables.Column(orderable=False, empty_values=())
    Tipo = tables.Column(orderable=False, empty_values=())
    FechaInsc = tables.Column(orderable=False, empty_values=())
    Anio = tables.Column(orderable=False, empty_values=())
    Interno = tables.Column(orderable=False, empty_values=())
    Capacidad = tables.Column(orderable=False, empty_values=())
    Marca = tables.Column(orderable=False, empty_values=())
    NumChasis = tables.Column(orderable=False, empty_values=())
    ModeloChasis = tables.Column(orderable=False, empty_values=())
    MarcaChasis = tables.Column(orderable=False, empty_values=())
    MotorNum = tables.Column(orderable=False, empty_values=())
    Empresa = tables.Column(orderable=False, empty_values=())
    Domicilio = tables.Column(orderable=False, empty_values=())
    CodPostal = tables.Column(orderable=False, empty_values=())
    Localidad = tables.Column(orderable=False, empty_values=())
    Responsable = tables.Column(orderable=False, empty_values=())
    DNIRespon = tables.Column(orderable=False, empty_values=())
    DomicRespon = tables.Column(orderable=False, empty_values=())
    TelRespon = tables.Column(orderable=False, empty_values=())


class ConsultaHabsTable(tables.Table):
    Hoy = tables.Column(orderable=False, empty_values=())
    InicHabilit = tables.Column(orderable=False, empty_values=())
    NumHabilit = tables.Column(orderable=False, empty_values=())
    VehiAnio = tables.Column(orderable=False, empty_values=())
    VehiCapac = tables.Column(orderable=False, empty_values=())
    VehiInt = tables.Column(orderable=False, empty_values=())
    VehiPat = tables.Column(orderable=False, empty_values=())
    VtoHabilit = tables.Column(orderable=False, empty_values=())
    VtoRevTec = tables.Column(orderable=False, empty_values=())
    VtoSeguro = tables.Column(orderable=False, empty_values=())
