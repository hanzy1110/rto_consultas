import django_tables2 as tables
from django.core.paginator import Paginator
from django.utils.html import format_html
from .models import (
    # VWVerificaciones,
    Localidades,
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
from .helpers import AuxData, map_fields, generate_key_from_params, convert_date

# from silk.profiling.profiler import silk_profile
from django.core.cache import cache

vals = {1: "Verdadero", 0: "Falso"}
vals_anulado = {1: "anulado", 0: "vigente"}


class ImageColumn(tables.Column):
    def render(self, record):
        cache_key = f"certificado:{record.idtaller}-{record.idverificacion}"

        cert = cache.get(cache_key, None)

        if not cert:
            cert = Certificados.objects.filter(
                idverificacion_id__exact=record.idverificacion,
                idtaller_id__exact=record.idtaller,
            ).values()

            cert = cert[0]

        key = vals_anulado[cert["anulado"]]

        # return format_html('<img src="{% static img/small-logos/{}.png}" />', key)
        return format_html('<img src="{% static img/small-logos/{}.png %}" />', key)


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


class VerificacionesTables(tables.Table):
    certificado = tables.Column(
        orderable=False,
        empty_values=(),
    )
    fecha = tables.DateColumn(verbose_name="Emision", format="d/m/Y")
    ver_verificacion = tables.Column(
        linkify=(
            "ver_verificacion",
            {
                "idverificacion": tables.A("idverificacion"),
                "idtaller": tables.A("idtaller__idtaller"),
            },
        ),
        orderable=False,
        empty_values=(),
    )  # (viewname, kwargs)
    ver_certificado = CustomFileColumn(
        orderable=False,
        empty_values=(),
    )  # (viewname, kwargs)
    titular = tables.Column(orderable=False, empty_values=())
    anulado = ImageColumn(orderable=False, empty_values=(), verbose_name="Estado")
    vigencia = tables.Column(orderable=False, empty_values=())
    idtaller = tables.Column(empty_values=(), verbose_name="Planta")
    idestado = tables.Column(empty_values=(), verbose_name="Calificación")
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
        return f"Ver Verificacion"

    def render_ver_certificado(self, record, value):
        cache_key = f"certificado:{record.idtaller_id}-{record.idverificacion}"
        cached_cert = cache.get(cache_key)
        if cached_cert:
            # nro_cert = Certificados.objects.get(idverificacion_id=record.idverificacion)
            return "Ver Certificado"
            # return str(nro_cert)
        else:
            # nro_cert = Certificados.objects.get(idverificacion_id=record.idverificacion)
            return "Ver Certificado"
            # return str(nro_cert)
        # return "No disponible"

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
            descriptions = map_fields(self.aux_data, self.Meta.model)
            return descriptions["idtipouso"][value]

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
