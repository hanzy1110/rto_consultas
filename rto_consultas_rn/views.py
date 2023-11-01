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
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordChangeView,
    PasswordResetConfirmView,
)
from django.http import HttpResponse
from django.template.loader import render_to_string

from django.contrib.auth.models import User

from wkhtmltopdf.views import PDFTemplateView

from datetime import date

from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django_tables2.export.export import TableExport
from django.contrib import messages

from admin_soft.forms import LoginForm

from .models import (
    Adjuntos,
    Localidades,
    Personas,
    Provincias,
    Usuarios,
    Verificaciones,
    Certificadosasignadosportaller,
    Vehiculos,
    Certificados,
    Categorias,
    Verificacionesdefectos,
    Verificacionespdf,
)
from rto_consultas_rn.models import Estados, Tipousovehiculo, Talleres
from rto_consultas_rn.tables import (
    ResumenTransporteCargaTable,
    ResumenTransporteTable,
    VerificacionesTables,
    VehiculosTable,
    CertificadosTable,
    CertificadosAssignTable,
    CertificadosTablesResumen,
    VerificacionesAnuales,
)
from rto_consultas.helpers import (
    filter_vup_transporte,
    generate_key_certificado,
    handle_context,
    handle_query,
    AuxData,
    generate_key,
    build_barcode,
    handle_save_hab,
)

from rto_consultas.forms import (
    ConsultaDPTForm,
    CustomRTOForm,
    ObleasPorTaller,
    InspectionOrderForm,
)  # Import the form you created

from rto_consultas.logging import configure_logger

LOG_FILE = os.environ["LOG_FILE"]
logger   = configure_logger(LOG_FILE)


@login_required
def rn_view(request):
    template_name = "pages/RN/index_rn.html"
    return render(request, template_name, {"segment": "index"})


@login_required
def dvr_view(request):
    template_name = "pages/RN/dvr_index.html"
    return render(request, template_name, {"segment": "index"})


@login_required
def secretaria_transporte_view(request):
    template_name = "pages/RN/index_rn_transporte.html"
    return render(request, template_name, {"segment": "index"})


class CustomRTOView(ExportMixin, SingleTableView, LoginRequiredMixin):
    model: Model
    paginate_by: int
    template_name: str
    context_object_name: str
    table_class: Table
    aux_data: AuxData
    partial_template: str

    def get_queryset(self):
        _export  = self.request.GET.copy().pop("_export", None)
        page     = self.request.GET.copy().pop("page", None)
        queryset = handle_query(self.request, self.model, self.aux_data.fecha_field)

        if page:
            # Handle pagination...
            self.table_data = queryset
            self.get_table()

        return queryset

    def get_context_data(self, **kwargs):
        # logger.debug("HANDLING CONTEXT...")
        context = super().get_context_data(**kwargs)
        context = handle_context(context, self)

        logger.debug("CONTEXT HANDLED...")
        return context

    def get_template_names(self):
        logger.debug("Checking for template...")
        if self.request.htmx:
            logger.debug("HTMX REQUEST!!")
            return [self.partial_template]
        return [self.template_name]


@method_decorator(login_required, name="dispatch")
class ListVerificacionesView(CustomRTOView):
    # authentication_classes = [authentication.TokenAuthentication]
    model                    = Verificaciones
    paginate_by              = 10
    template_name = "includes/list_table_verificaciones.html"
    context_object_name = "Verificaciones"
    table_class              = VerificacionesTables
    partial_template = "includes/table_view.html"
    form_class               = CustomRTOForm

    aux_data = AuxData(
        query_fields = [
            "dominiovehiculo",
            "nrocertificado",
            "fecha_desde",
            "fecha_hasta",
            "dni",
            "nrodoc",
        ],
        form_fields={
            "idestado": ("descripcion", Estados),
            "idtipouso": ("descripcion", Tipousovehiculo),
            "idtaller": ("nombre", Talleres),
            "anulado": (None, None),
        },
        parsed_names = {
            "dominiovehiculo": "Dominio",
            "idestado": "Calificación",
            "idtipouso": "Tipo Uso Vehiculo",
            "nrocertificado": "Nro. Certificado",
            "fecha_desde": "Fecha Desde",
            "fecha_hasta": "Fecha Hasta",
            "idtaller": "Planta",
            "anulado": "Anulado",
            "dni": "DNI",
            "nrodoc": "Nro. Doc.",
        },
        ids={
            "dominiovehiculo": "#txtDominio",
            "fecha_desde": "#txtFechaD",
            "fecha_hasta": "#txtFechaH",
            "nrocertificado": "Nro. Certificado",
            "idestado": "#slctIdEstado",
            "idtipouso": "#slctIdTipouso",
            "idtaller": "#slctIdtaller",
            "anulado": "#slctAnulado",
        },
        types        = {
            "dominiovehiculo": "text",
            "fecha_desde": "date",
            "fecha_hasta": "date",
            "nrocertificado": "text",
            "dni": "select",
        },
        render_url   = "verificaciones",
    )

    def get_queryset(self):
        logger.info("CALCULATE QUERYSET...")
        queryset     = super().get_queryset()
        if isinstance(queryset, list):
            pass
            queryset = list(reversed(queryset))
        else:
            queryset = queryset.order_by("-idverificacion")
        logger.info("QUERYSET DONE...")
        return queryset

@method_decorator(login_required, name = "dispatch")
class VerVerificacion(DetailView, LoginRequiredMixin):
    model: Verificaciones
    template_name                      = "includes/ver_verificaciones.html"
    context_object_name: str
    aux_data: AuxData

    def get_object(self):
        query_params         = self.request.GET.copy()
        id_taller            = self.kwargs["idtaller"]
        id_verificacion      = self.kwargs["idverificacion"]
        verificacion         = Verificaciones.objects.select_related(
            "dominiovehiculo", "idestado", "codigotitular", "idtaller"
        ).get(idverificacion = id_verificacion, idtaller=id_taller)

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
        MToFI   = sum_appropriatelly(
            [
                self.verificacion.eje1_fzaizq,
                self.verificacion.eje2_fzaizq,
                self.verificacion.eje3_fzaizq,
                self.verificacion.eje4_fzaizq,
            ]
        )
        MToFD   = sum_appropriatelly(
            [
                self.verificacion.eje1_fzader,
                self.verificacion.eje2_fzader,
                self.verificacion.eje3_fzader,
                self.verificacion.eje4_fzader,
            ]
        )
        MToEf   = round((((MToFI + MToFD) / (MToTara * 9.81)) * 100), 2)
        return MToTara, MToFI, MToFD, MToEf

    def get_context_data(self, **kwargs):
        context                          = super().get_context_data(**kwargs)
        cert                             = (
            Certificados.objects
            # .select_related("idcategoria")
            .filter(
                idverificacion_id__exact = self.kwargs["idverificacion"],
                idtaller_id__exact       = self.kwargs["idtaller"],
            ).values()
        )
        categoria                        = Categorias.objects.get(
            idcategoria__exact           = cert[0]["idcategoria"]
        ).descripcion

        estado = Estados.objects.get(idestado__exact = cert[0]["idestado"]).descripcion

        localidad              = Localidades.objects.get(
            idlocalidad__exact = self.verificacion.pidlocalidad
        )

        adjuntos = Adjuntos.objects.filter(
            idtaller__exact       = cert[0]["idtaller_id"],
            idverificacion__exact = cert[0]["idverificacion_id"],
        )

        defectos = Verificacionesdefectos.objects.prefetch_related("idnivel").filter(
            idtaller_id__exact=cert[0]["idtaller_id"],
            idverificacion_id__exact = cert[0]["idverificacion_id"],
        )

        pdf_certificado              = Verificacionespdf.objects.filter(
            idtaller_id__exact       = cert[0]["idtaller_id"],
            idverificacion_id__exact = cert[0]["idverificacion_id"],
        )

        print(defectos)

        context["nrocertificado"] = cert[0]["nrocertificado"]
        context["observaciones"]  = cert[0]["observaciones"]
        context["vigenciahasta"]  = cert[0]["vigenciahasta"]
        context["estado"]         = estado
        context["categoria"]      = categoria
        context["provincia"]      = localidad.idprovincia.descripcion
        context["localidad"]      = localidad.descripcion

        adjuntos = [generate_key(a) for a in adjuntos]
        context["certificado"] = cert[0]
        context["url_certificado"] = generate_key_certificado(pdf_certificado)
        context["adjuntos"]        = adjuntos
        context["defectos"] = defectos
        context["mostrarJu"]       = ""
        context["mostrarFi"]       = ""

        MToTara, MToFI, MToFD, MToEf = self.get_total_values()
        context["mto_tara"]          = MToTara
        context["mto_fi"] = MToFI
        context["mto_der"]           = MToFD
        context["mto_eficiencia"]    = MToEf

        # context = handle_context(context, self)
        return context
