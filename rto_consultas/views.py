import os
from django.db.models import Model, Prefetch
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.base import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_tables2 import SingleTableView, Table
from django_tables2.export.views import ExportMixin
from django_tables2.export.export import TableExport
from django.forms.models import model_to_dict

from datetime import date
from django_tables2.config import RequestConfig
from django_tables2.export.export import TableExport
from django.db.models import Q

from functools import reduce

from .models import (
    Adjuntos,
    Localidades,
    Provincias,
    Verificaciones,
    Certificadosasignadosportaller,
    Vehiculos,
    Certificados,
    Categorias,
    Verificacionesdefectos,
    Verificacionespdf,
)
from .models import Estados, Tipousovehiculo, Talleres
from .tables import (
    ObleasPorTallerTable,
    ResumenTransporteCargaTable,
    ResumenTransporteTable,
    VerificacionesTables,
    VehiculosTable,
    CertificadosTable,
    CertificadosAssignTable,
    CertificadosTablesResumen,
    VerificacionesAnuales,
)
from .helpers import (
    filter_vup_transporte,
    generate_key_certificado,
    handle_context,
    handle_query,
    AuxData,
    generate_key,
)

from .forms import ObleasPorTaller

from .logging import configure_logger

LOG_FILE = os.environ["LOG_FILE"]
logger = configure_logger(LOG_FILE)

# from .presigned_url import generate_presigned_url


class CustomRTOView(ExportMixin, SingleTableView, LoginRequiredMixin):
    model: Model
    paginate_by: int
    template_name: str
    context_object_name: str
    table_class: Table
    aux_data: AuxData
    partial_template: str

    def get_queryset(self):
        _export = self.request.GET.copy().pop("_export", None)
        page = self.request.GET.copy().pop("page", None)
        queryset = handle_query(self.request, self.model, self.aux_data.fecha_field)

        if page:
            # Handle pagination...
            self.table_data = queryset
            self.get_table()

        return queryset

    def get_context_data(self, **kwargs):
        logger.debug("HANDLING CONTEXT...")
        context = super().get_context_data(**kwargs)
        context = handle_context(context, self)
        return context

    def get_template_names(self):
        logger.debug("Checking for template...")
        if self.request.htmx:
            logger.debug("HTMX REQUEST!!")
            return [self.partial_template]
        return [self.template_name]


class ListVerificacionesView(CustomRTOView):
    # authentication_classes = [authentication.TokenAuthentication]
    model = Verificaciones
    paginate_by = 10
    template_name = "includes/list_table_verificaciones.html"
    context_object_name = "Verificaciones"
    table_class = VerificacionesTables
    partial_template = "includes/table_view.html"

    aux_data = AuxData(
        query_fields=[
            "dominiovehiculo",
            "nrocertificado",
            "fecha_desde",
            "fecha_hasta",
        ],
        form_fields={
            "idestado": ("descripcion", Estados),
            "idtipouso": ("descripcion", Tipousovehiculo),
            "idtaller": ("nombre", Talleres),
            "anulado": (None, None),
        },
        parsed_names={
            "dominiovehiculo": "Dominio Vehiculo",
            "idestado": "Estado Certificado",
            "idtipouso": "Tipo Uso Vehiculo",
            "nrocertificado": "Nro. Certificado",
            "fecha_desde": "Fecha Desde",
            "fecha_hasta": "Fecha Hasta",
            "idtaller": "Nombre Taller",
            "anulado": "Anulado",
        },
        ids={
            "dominiovehiculo": "#txtDominio",
            "fecha_desde": "#txtFechaD",
            "fecha_hasta": "#txtFechaH",
            "nrocertificado": "Nro. Certificado",
        },
        types={
            "dominiovehiculo": "text",
            "fecha_desde": "date",
            "fecha_hasta": "date",
            "nrocertificado": "text",
        },
        render_url="verificaciones",
    )

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     cert_queries = [
    #         Q(idtaller_id=q.idtaller_id, idverificacion_id=q.idverificacion)
    #         for q in queryset
    #     ]
    #     query = reduce(lambda x, y: x and y, cert_queries)
    #     certs = Certificados.objects.filter(query)
    #     certs_no_anulados = Certificados.objects.filter(anulado__exact=0)
    #     return certs.intersection(certs_no_anulados)


class CargaObleas(CustomRTOView):
    # authentication_classes = [authentication.TokenAuthentication]
    model = Certificadosasignadosportaller
    paginate_by = 10
    template_name = "includes/list_table.html"
    context_object_name = "Certificados Asignados por taller"
    table_class = CertificadosAssignTable
    partial_template = "includes/table_view.html"

    aux_data = AuxData(
        query_fields=[
            "cert_init",
            "cert_end",
        ],
        form_fields={
            "idtaller": ("nombre", Talleres),
        },
        parsed_names={
            "idtaller": "Nombre Taller",
            "cert_init": "Nro Oblea desde",
            "cert_end": "Nro Oblea hasta",
        },
        ids={},
        types={
            "cert_init": "text",
            "cert_end": "text",
        },
        fecha_field="fechacarga",
        render_url="carga_obleas",
    )


class ResumenObleas(CustomRTOView, LoginRequiredMixin):
    model = Certificadosasignadosportaller
    paginate_by = 10
    template_name = "includes/list_table.html"
    context_object_name = "Certificados Asignados por taller"
    table_class = ObleasPorTaller
    partial_template = "includes/table_view.html"

    aux_data = AuxData(
        query_fields=[
            "fecha_desde",
            "fecha_hasta",
        ],
        form_fields={
            "idtaller": ("nombre", Talleres),
        },
        parsed_names={
            "idtaller": "Nombre Taller",
            "fecha_desde": "Fecha Desde",
            "fecha_hasta": "Fecha Hasta",
        },
        ids={
            "fecha_desde": "#txtFechaD",
            "fecha_hasta": "#txtFechaH",
        },
        types={
            "fecha_desde": "date",
            "fecha_hasta": "date",
            "nrocertificado": "text",
        },
        fecha_field="fechacarga",
        render_url="resumen_obleas",
    )

    def get_context_data(self):
        context = super().get_context_data()

        data = []
        talleres = Talleres.objects.all()
        if self.request.GET:
            idtaller = self.request.GET.get("taller", None)
            talleres = Talleres.objects.filter(idtaller__iexact=idtaller)

        for t in talleres:
            certs_by_taller = Certificadosasignadosportaller.objects.filter(
                idtaller=t.idtaller, disponible__iexact=1
            )

            cert_data = filter_vup_transporte(certs_by_taller)
            cert_data["taller"] = t.nombre

            data.append(cert_data)

        logger.info(data)
        table = ObleasPorTaller(data)
        context["table"] = table

        return context


class ListCertificadosAssignView(CustomRTOView):
    # authentication_classes = [authentication.TokenAuthentication]
    model = Certificadosasignadosportaller
    paginate_by = 10
    template_name = "includes/list_table.html"
    context_object_name = "Certificados Asignados por taller"
    table_class = CertificadosAssignTable
    partial_template = "includes/table_view.html"

    aux_data = AuxData(
        query_fields=[
            "nrocertificado",
            "fecha_desde",
            "fecha_hasta",
            # "cert_init",
            # "cert_end",
        ],
        form_fields={
            "idtaller": ("nombre", Talleres),
            "disponible": (None, None),
            "replicado": (None, None),
        },
        parsed_names={
            "nrocertificado": "Nro. Certificado",
            "disponible": "Disponible",
            "idtaller": "Nombre Taller",
            "replicado": "Replicado",
            "fecha_desde": "Fecha Desde",
            "fecha_hasta": "Fecha Hasta",
            # "cert_init": "Nro Oblea desde",
            # "cert_end": "Nro Oblea hasta",
        },
        ids={
            "nrocertificado": "#txtNroCertificado",
            "fecha_desde": "#txtFechaD",
            "fecha_hasta": "#txtFechaH",
        },
        types={
            "fecha_desde": "date",
            "fecha_hasta": "date",
            "nrocertificado": "text",
            # "cert_init": "text",
            # "cert_end": "text",
        },
        fecha_field="fechacarga",
        render_url="certs_asignados",
    )


class ListVehiculosView(CustomRTOView):
    # authentication_classes = [authentication.TokenAuthentication]
    model = Vehiculos
    template_name = "includes/list_table.html"
    paginate_by = 10
    context_object_name = "Vehiculos"
    table_class = VehiculosTable

    aux_data = AuxData(
        query_fields=["dominio", "marca"],
        form_fields={"idtipouso": ("descripcion", Tipousovehiculo)},
        parsed_names={
            "dominio": "Dominio Vehiculo",
            "marca": "Marca Vehiculo",
            "idtipouso": "Tipo Uso Vehiculo",
        },
        ids={"dominiovehiculo": "#txtDominio", "marca": "#txtMarca"},
        types={
            "marca": "text",
            "dominio": "text",
        },
    )


class ListCertificadosView(CustomRTOView):
    # authentication_classes = [authentication.TokenAuthentication]
    model = Certificados
    template_name = "includes/list_table.html"
    paginate_by = 10
    context_object_name = "Certificados"
    table_class = CertificadosTable

    aux_data = AuxData(
        query_fields=["nrocertificado", "fecha", "anulado"],
        form_fields={"idtaller": ("nombre", Talleres)},
        parsed_names={
            "nrocertificado": "Nro. Certificado",
            "anulado": "Anulado",
            "fecha": "Fecha",
            "idtaller": "Nombre Taller",
        },
        ids={
            "nrocertificado": "#txtNroCertificado",
            "fecha": "#txtFechaD",
        },
        types={
            "nrocertificado": "text",
            "fecha": "date",
            "anulado": "text",
        },
    )


class ListarVerificacionesTotales(CustomRTOView, ExportMixin):
    # authentication_classes = [authentication.TokenAuthentication]
    model = Certificados
    paginate_by = 10
    template_name = "includes/list_table_verificaciones.html"
    context_object_name = "Verificaciones"
    table_class = CertificadosTablesResumen
    export_formats = ["csv", "tsv", "xls"]
    table_name = "resumen_verificaciones"

    aux_data = AuxData(
        query_fields=[
            # "dominiovehiculo",
            "nrocertificado",
            "fecha_desde",
            "fecha_hasta",
        ],
        form_fields={
            "idestado": ("descripcion", Estados),
            # "idtipouso": ("descripcion", Tipousovehiculo),
            "idtaller": ("nombre", Talleres),
        },
        parsed_names={
            # "dominiovehiculo": "Dominio Vehiculo",
            "idestado": "Estado Certificado",
            # "idtipouso": "Tipo Uso Vehiculo",
            "nrocertificado": "Nro. Certificado",
            "fecha_desde": "Fecha Desde",
            "fecha_hasta": "Fecha Hasta",
            "idtaller": "Nombre Taller",
        },
        ids={
            # "dominiovehiculo": "#txtDominio",
            "fecha_desde": "#txtFechaD",
            "fecha_hasta": "#txtFechaH",
            "nrocertificado": "Nro. Certificado",
        },
        types={
            # "dominiovehiculo": "text",
            "fecha_desde": "date",
            "fecha_hasta": "date",
            "nrocertificado": "text",
        },
        aux={"Button": "DESCARGAR"},
    )


class VerVerificacion(DetailView, LoginRequiredMixin):
    model: Verificaciones
    template_name = "includes/ver_verificaciones.html"
    context_object_name: str
    aux_data: AuxData

    def get_object(self):
        query_params = self.request.GET.copy()
        id_taller = self.kwargs["idtaller"]
        id_verificacion = self.kwargs["idverificacion"]
        verificacion = Verificaciones.objects.select_related(
            "dominiovehiculo", "idestado", "codigotitular", "idtaller"
        ).get(idverificacion=id_verificacion, idtaller=id_taller)

        print(verificacion)
        self.verificacion = verificacion
        return verificacion

    def get_total_values(
        self,
    ):
        def sum_appropriatelly(values):
            return sum([float(v) for v in values if v])

        MToTara = sum_appropriatelly(
            [
                self.verificacion.eje1_tara,
                self.verificacion.eje2_tara,
                self.verificacion.eje3_tara,
                self.verificacion.eje4_tara,
            ]
        )
        MToFI = sum_appropriatelly(
            [
                self.verificacion.eje1_fzaizq,
                self.verificacion.eje2_fzaizq,
                self.verificacion.eje3_fzaizq,
                self.verificacion.eje4_fzaizq,
            ]
        )
        MToFD = sum_appropriatelly(
            [
                self.verificacion.eje1_fzader,
                self.verificacion.eje2_fzader,
                self.verificacion.eje3_fzader,
                self.verificacion.eje4_fzader,
            ]
        )
        MToEf = round((((MToFI + MToFD) / (MToTara * 9.81)) * 100), 2)
        return MToTara, MToFI, MToFD, MToEf

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cert = (
            Certificados.objects
            # .select_related("idcategoria")
            .filter(
                idverificacion_id__exact=self.kwargs["idverificacion"],
                idtaller_id__exact=self.kwargs["idtaller"],
            ).values()
        )
        categoria = Categorias.objects.get(
            idcategoria__exact=cert[0]["idcategoria"]
        ).descripcion

        estado = Estados.objects.get(idestado__exact=cert[0]["idestado"]).descripcion

        localidad = Localidades.objects.get(
            idlocalidad__exact=self.verificacion.pidlocalidad
        )

        adjuntos = Adjuntos.objects.filter(
            idtaller__exact=cert[0]["idtaller_id"],
            idverificacion__exact=cert[0]["idverificacion_id"],
        )

        defectos = Verificacionesdefectos.objects.prefetch_related("idnivel").filter(
            idtaller_id__exact=cert[0]["idtaller_id"],
            idverificacion_id__exact=cert[0]["idverificacion_id"],
        )

        pdf_certificado = Verificacionespdf.objects.filter(
            idtaller_id__exact=cert[0]["idtaller_id"],
            idverificacion_id__exact=cert[0]["idverificacion_id"],
        )

        print(defectos)

        context["nrocertificado"] = cert[0]["nrocertificado"]
        context["observaciones"] = cert[0]["observaciones"]
        context["vigenciahasta"] = cert[0]["vigenciahasta"]
        context["estado"] = estado
        context["categoria"] = categoria
        context["provincia"] = localidad.idprovincia.descripcion
        context["localidad"] = localidad.descripcion

        adjuntos = [generate_key(a) for a in adjuntos]
        context["certificado"] = cert[0]
        context["url_certificado"] = generate_key_certificado(pdf_certificado)
        context["adjuntos"] = adjuntos
        context["defectos"] = defectos
        context["mostrarJu"] = ""
        context["mostrarFi"] = ""

        MToTara, MToFI, MToFD, MToEf = self.get_total_values()
        context["mto_tara"] = MToTara
        context["mto_fi"] = MToFI
        context["mto_der"] = MToFD
        context["mto_eficiencia"] = MToEf

        # context = handle_context(context, self)
        return context


def resumen_obleas(request):
    if request.htmx:
        logger.info("RENDERING HTMX!")
        data = []
        talleres = Talleres.objects.all()
        idtaller = request.GET.get("taller", None)
        if idtaller:
            talleres = Talleres.objects.filter(idtaller__iexact=idtaller)

        for t in talleres:
            certs_by_taller = Certificadosasignadosportaller.objects.filter(
                idtaller=t.idtaller, disponible__iexact=1
            )

            cert_data = filter_vup_transporte(certs_by_taller)
            cert_data["taller"] = t.nombre

            data.append(cert_data)

        logger.debug(talleres)
        logger.debug(data)
        table = ObleasPorTallerTable(data)
        return render(request, "includes/table_view.html", {"table": table})

    form = ObleasPorTaller()
    return render(request, "includes/consulta_obleas.html", {"form": form})


def verificaciones_anuales(request):
    data = []
    for year in range(2015, 2023):
        current = {}
        start_date = date(year, 1, 1)
        end_date = date(year, 12, 31)
        current["year"] = year
        current["cant_verificaciones"] = Verificaciones.objects.filter(
            fecha__range=(start_date, end_date)
        ).count()

        current["cant_aprobados"] = Certificados.objects.filter(
            fecha__range=(start_date, end_date), idestado__exact=1
        ).count()

        current["cant_aprobados_condicionales"] = Certificados.objects.filter(
            fecha__range=(start_date, end_date), idestado__exact=2
        ).count()

        current["cant_rechazados"] = Certificados.objects.filter(
            fecha__range=(start_date, end_date), idestado__exact=3
        ).count()
        data.append(current)
    table = VerificacionesAnuales(data)

    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response(f"table.{export_format}")

    return render(request, "includes/table_view.html", {"table": table})


class ResumenTransportePasajeros(CustomRTOView):
    # authentication_classes = [authentication.TokenAuthentication]
    model = Verificaciones
    paginate_by = 10
    template_name = "includes/list_table_verificaciones.html"
    context_object_name = "Verificaciones"
    table_class = ResumenTransporteTable

    aux_data = AuxData(
        query_fields=[
            "fecha_desde",
            "fecha_hasta",
        ],
        form_fields={
            "idestado": ("descripcion", Estados),
            "idtipouso": ("descripcion", Tipousovehiculo),
            "idtaller": ("nombre", Talleres),
        },
        parsed_names={
            "idestado": "Estado Certificado",
            "idtipouso": "Tipo Uso Vehiculo",
            "fecha_desde": "Fecha Desde",
            "fecha_hasta": "Fecha Hasta",
            "idtaller": "Nombre Taller",
        },
        ids={
            "fecha_desde": "#txtFechaD",
            "fecha_hasta": "#txtFechaH",
        },
        types={
            "fecha_desde": "date",
            "fecha_hasta": "date",
        },
    )


class ResumenTransporteCarga(CustomRTOView):
    # authentication_classes = [authentication.TokenAuthentication]
    model = Verificaciones
    paginate_by = 10
    template_name = "includes/list_table_verificaciones.html"
    context_object_name = "Verificaciones"
    table_class = ResumenTransporteCargaTable

    aux_data = AuxData(
        query_fields=[
            "fecha_desde",
            "fecha_hasta",
        ],
        form_fields={
            "idestado": ("descripcion", Estados),
            "idtipouso": ("descripcion", Tipousovehiculo),
            "idtaller": ("nombre", Talleres),
        },
        parsed_names={
            "idestado": "Estado Certificado",
            "idtipouso": "Tipo Uso Vehiculo",
            "fecha_desde": "Fecha Desde",
            "fecha_hasta": "Fecha Hasta",
            "idtaller": "Nombre Taller",
        },
        ids={
            "fecha_desde": "#txtFechaD",
            "fecha_hasta": "#txtFechaH",
        },
        types={
            "fecha_desde": "date",
            "fecha_hasta": "date",
        },
    )
