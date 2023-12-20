from collections.abc import Callable
import os
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db.models import Count, Model, Prefetch
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views import View
from django.views.generic.base import RedirectView, TemplateView
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
from django.http import HttpHeaders, HttpResponse, JsonResponse
from django.template.loader import render_to_string

from django.contrib.auth.models import User

from wkhtmltopdf.views import PDFTemplateView

from datetime import date, datetime, timedelta

from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django_tables2.export.export import TableExport
from django.contrib import messages

from admin_soft.forms import LoginForm

from .models import (
    Adjuntos,
    Habilitacion,
    Localidades,
    Personas,
    Provincias,
    Serviciohab,
    Serviciostransportehab,
    Usuarios,
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
    ConsultaDPTTable,
    ConsultaHabsTable,
    HabilitacionesTable,
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
    CertBoundError,
    filter_vup_transporte,
    generate_key_certificado,
    get_queryset_from_user,
    get_resumen_data_mensual,
    get_template_from_user,
    get_tipo_uso_by_user,
    handle_context,
    handle_query,
    AuxData,
    generate_key,
    build_barcode,
    handle_resumen_context,
    handle_save_hab,
    handle_initial_hab,
)

from .forms import (
    ConsultaDPTForm,
    CustomRTOForm,
    ObleasPorTaller,
    InspectionOrderForm,
    ResumenMensualDPT,
    ResumenMensualForm,
    ResumenMensualSV,
    route_form,
)  # Import the form you created

from .consultas_dpt import HabsResponse, query_dpt, DPTResponse

from .logging import configure_logger, print_stack
from .name_schemas import *

LOG_FILE = os.environ["LOG_FILE"]
logger = configure_logger(LOG_FILE)


@login_required
def nqn_view(request):
    template_name = "pages/index_nqn.html"
    return render(request, template_name, {"segment": "index"})


@login_required
def index(request):
    user = request.user
    # Check the user's group or any other condition
    template_name = "pages/index.html"
    # if user.groups.filter(name="DPTGroup").exists():
    #     template_name = "pages/dpt_index.html"
    # elif user.groups.filter(name="SVGroup").exists():
    #     template_name = "pages/sv_index.html"

    return render(request, template_name, {"segment": "index"})


# Authentication
class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    form_class = LoginForm


def logout_view(request):
    logout(request)
    return redirect("login")


def empty_view(request):
    if request.method == "GET":
        return HttpResponse("")


@method_decorator(csrf_exempt, name="dispatch")
class ChangeModelView(View):
    model: Model
    id_param: str
    delete_msg: str
    msg_estado: str
    table_view: str
    operation: Callable

    def post(self, request, *args, **kwargs):
        model_id = request.POST.get(
            self.id_param, None
        )  # Assuming the ID is sent through a POST request

        if not model_id:
            model_id = kwargs.get(self.id_param)

        # Fetch the related model instance
        model_instance = get_object_or_404(self.model, **{self.id_param: model_id})

        # Delete the model instance
        res = self.operation(model_instance)

        if res:
            messages.success(request, f"{self.delete_msg} {model_id} {self.msg_estado}")
        else:
            messages.error(request, "Error al Anular certificado")
        response = {
            "messages": [m.message for m in messages.get_messages(request)][-1],
        }

        res = HttpResponse(
            render_to_string(
                template_name="tables/table_messages.html", context=response
            )
        )
        res.headers["HX-Trigger"] = "reloadTable"
        return res


@method_decorator(login_required, name="dispatch")
class IndexView(TemplateView):
    urls: dict[str, str]
    template_name = "includes/generic_index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["urls"] = self.urls
        return context


class DPTView(IndexView):
    urls = {
        "verificaciones": "Verificaciones",
        "consulta_ordenes_insp": "Consulta Órdenes de Inspección",
        "cccf": "Consulta CCCF",
        "carga_obleas": "Carga Obleas",
        "consulta_resumen_mensual": "Resumen de Inspecciones",
    }


class HabsView(IndexView):
    urls = {
        "carga_habilitacion": "Carga Órdenes de Inspección",
        "habilitaciones": "Consulta Órdenes de Inspección",
        "consulta_habilitaciones_finales": "Consulta DPT",
    }


class SVViewAuditoria(IndexView):
    urls = {
        "verificaciones": "Verificaciones",
        "consulta_documentacion": "Consulta Documentacion",
        "consulta_resumen_mensual": "Resumen de Inspecciones",
    }


class SVView(IndexView):
    urls = {
        "verificaciones": "Verificaciones",
        "carga_obleas": "Carga Obleas",
        "consulta_resumen_mensual": "Resumen de Inspecciones",
    }


class DocumentView(IndexView):
    urls = {
        "certs_asignados": "Certificados Asignados",
        "carga_obleas": "Carga Obleas",
        "resumen_obleas": "Consulta Disponibilidad Obleas",
    }


def get_template_name(request, *args, **kwargs):
    # TODO Change the default!
    if request.htmx:
        width = request.GET.get("width", None)

        if not width:
            width = kwargs.pop("width", -1)
        width = int(width)

        logger.debug(f"WIDTH WAS => {width}")

        # TODO additional routing depending on size
        template_name = get_template_from_user(request)
        logger.info(f"TEMPLATE NAME => {template_name}")

        # if width <= 768 and width > -1:
        #     template_name = "pages/index_small.html"
        # elif width >= 768 and width < 1024:
        #     template_name = "index_medium.html"
        # else:
        #     template_name = "index_large.html"

        # return JsonResponse({"template_name": template_name})
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
        _export = self.request.GET.copy().pop("_export", None)
        page = self.request.GET.copy().pop("page", None)
        queryset = handle_query(self.request, self.model, self.aux_data.fecha_field)
        if self.model == Verificaciones:
            queryset = get_queryset_from_user(queryset, self.request)
        # elif self.model == Certificadosasignadosportaller:
        #     queryset = get_queryset_from_user(
        #         queryset, self.request, model="certs_asignados"
        #     )

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

    def get(self, request, *args, **kwargs):
        try:
            logger.debug(f"KWARGS ==> {kwargs}")
            response = super().get(request, *args, **kwargs)
            return response
        except CertBoundError as e:
            logger.error("ERROR DURING QUERY CERT BOUNDS...")
            logger.error(e.__cause__)
            res = HttpResponse("")
            res.headers["Hx-Trigger"] = "certBoundError"
            return res

    def get_template_names(self):
        if self.request.htmx:
            return [self.partial_template]
        return [self.template_name]


@method_decorator(login_required, name="dispatch")
class ListVerificacionesView(CustomRTOView):
    # authentication_classes = [authentication.TokenAuthentication]
    model = Verificaciones
    paginate_by = settings.PAGINATION
    template_name = "includes/list_table.html"
    context_object_name = "Verificaciones"
    table_class = VerificacionesTables
    partial_template = "includes/table_view.html"
    form_class = CustomRTOForm

    aux_data = AuxData(
        query_fields=[
            "dominiovehiculo",
        ],
        form_fields={},
        parsed_names={
            "dominiovehiculo": "Dominio",
        },
        ids={
            "dominiovehiculo": "#txtDominio",
        },
        types={
            "dominiovehiculo": "text",
        },
        render_url="verificaciones",
        render_form="verificaciones_form",
    )

    def get_queryset(self):
        logger.info("CALCULATE QUERYSET...")
        queryset = super().get_queryset()
        if isinstance(queryset, list):
            queryset = list(reversed(queryset))
        else:
            queryset = queryset.order_by("-idverificacion")
            queryset = queryset.order_by("-fecha")

        logger.info("QUERYSET DONE...")

        queryset = get_queryset_from_user(queryset, self.request)
        return queryset


def cert_bound_error(request, *args, **kwargs):
    return render(template_name="pages/cert_bound_error.html", request=request)


@method_decorator(login_required, name="dispatch")
class RenderVerificacionForm(TemplateView):
    template_name = "includes/form_render.html"

    aux_data = AuxData(
        query_fields=[
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
        parsed_names={
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
        types={
            "dominiovehiculo": "text",
            "fecha_desde": "date",
            "fecha_hasta": "date",
            "nrocertificado": "text",
            "dni": "select",
        },
        render_url="verificaciones",
    )

    form_class = CustomRTOForm
    model = Verificaciones

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = handle_context(context, self)
        return context


@method_decorator(login_required, name="dispatch")
class CargaObleas(CustomRTOView):
    # authentication_classes           = [authentication.TokenAuthentication]
    model = Certificadosasignadosportaller
    paginate_by = settings.PAGINATION
    template_name = "includes/list_table.html"
    context_object_name = "Certificados Asignados por taller"
    table_class = CertificadosAssignTable
    partial_template = "includes/table_view.html"
    form_class = CustomRTOForm

    aux_data = AuxData(
        query_fields=[
            "cert_init",
            "cert_end",
        ],
        form_fields={
            "idtaller": ("nombre", Talleres),
        },
        parsed_names={
            "idtaller": "Planta",
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


@method_decorator(login_required, name="dispatch")
class ResumenObleas(CustomRTOView, LoginRequiredMixin):
    model = Certificadosasignadosportaller
    paginate_by = settings.PAGINATION
    template_name = "includes/list_table.html"
    context_object_name = "Certificados Asignados por taller"
    table_class = ObleasPorTaller
    partial_template = "includes/table_view.html"
    form_class = CustomRTOForm

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


@method_decorator(login_required, name="dispatch")
class ListCertificadosAssignView(CustomRTOView):
    # authentication_classes           = [authentication.TokenAuthentication]
    model = Certificadosasignadosportaller
    paginate_by = settings.PAGINATION
    template_name = "includes/list_table.html"
    context_object_name = "Certificados Asignados por taller"
    table_class = CertificadosAssignTable
    partial_template = "includes/table_view.html"
    form_class = CustomRTOForm

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


@method_decorator(login_required, name="dispatch")
class ListHabilitaciones(CustomRTOView):
    # authentication_classes           = [authentication.TokenAuthentication]
    model = Habilitacion
    template_name = "includes/list_table.html"
    paginate_by = settings.PAGINATION
    context_object_name = "Habilitaciones"
    table_class = HabilitacionesTable
    partial_template = "includes/table_view.html"
    form_class = CustomRTOForm

    aux_data = AuxData(
        query_fields=[
            "dominio",
        ],
        form_fields={},
        parsed_names={
            "dominio": "Dominio Vehiculo",
        },
        ids={
            "dominiovehiculo": "#txtDominio",
        },
        types={
            "dominio": "text",
        },
        render_url="habilitaciones",
        render_form="habilitaciones_form",
    )


@method_decorator(login_required, name="dispatch")
class RenderHabilitacionForm(TemplateView):
    template_name = "includes/form_render.html"

    aux_data = AuxData(
        query_fields=[
            "dominio",
            "nrocodigobarrashab",
            "usuario",
            "fecha_desde",
            "fecha_hasta",
        ],
        form_fields={},
        parsed_names={
            "dominio": "Dominio Vehiculo",
            "nrocodigobarrashab": "Nro. Orden de Inspección",
            "usuario": "Usuario",
            "fecha_desde": "Fecha Desde",
            "fecha_hasta": "Fecha Hasta",
        },
        ids={"dominiovehiculo": "#txtDominio", "nrocodigobarrashab": "#txtNro"},
        types={
            "dominio": "text",
            "nrocodigobarrashab": "text",
            "fecha_desde": "date",
            "fecha_hasta": "date",
        },
        render_url="habilitaciones",
    )

    form_class = CustomRTOForm
    model = Verificaciones

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = handle_context(context, self)
        return context


@method_decorator(login_required, name="dispatch")
class ListVehiculosView(CustomRTOView):
    # authentication_classes           = [authentication.TokenAuthentication]
    model = Vehiculos
    template_name = "includes/list_table.html"
    paginate_by = settings.PAGINATION
    context_object_name = "Vehiculos"
    table_class = VehiculosTable
    partial_template = "includes/table_view.html"
    form_class = CustomRTOForm

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
        render_url="vehiculos",
    )


@method_decorator(login_required, name="dispatch")
class ListCertificadosView(CustomRTOView):
    # authentication_classes = [authentication.TokenAuthentication]
    model = Certificados
    template_name = "includes/list_table.html"
    paginate_by = settings.PAGINATION
    context_object_name = "Certificados"
    table_class = CertificadosTable
    partial_template = "includes/table_view.html"
    form_class = CustomRTOForm

    aux_data = AuxData(
        query_fields=["nrocertificado", "fecha", "anulado"],
        form_fields={
            "idtaller": ("nombre", Talleres),
            "anulado": (None, None),
        },
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
        },
        render_url="certificados",
    )


@method_decorator(login_required, name="dispatch")
class ListarVerificacionesTotales(CustomRTOView, ExportMixin):
    # authentication_classes = [authentication.TokenAuthentication]
    model = Certificados
    paginate_by = settings.PAGINATION
    template_name = "includes/list_table_verificaciones.html"
    context_object_name = "Verificaciones"
    table_class = CertificadosTablesResumen
    export_formats = ["csv", "tsv", "xls"]
    table_name = "resumen_verificaciones"
    form_class = CustomRTOForm

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


@method_decorator(login_required, name="dispatch")
class VerHabilitacion(DetailView, LoginRequiredMixin):
    model: Verificaciones
    template_name = "includes/ver_habilitaciones.html"
    context_object_name: str
    aux_data: AuxData

    def get_object(self):
        query_params = self.request.GET.copy()
        id_habilitacion = self.kwargs["idhabilitacion"]
        dominio = self.kwargs["dominio"]
        habilitacion = Habilitacion.objects.get(
            idhabilitacion=id_habilitacion, dominio=dominio
        )
        print(habilitacion)
        self.habilitacion = habilitacion
        return habilitacion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        id_habilitacion = self.kwargs["idhabilitacion"]
        dominio = self.kwargs["dominio"]
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
        return context


@method_decorator(login_required, name="dispatch")
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


class AuditarRevision(VerVerificacion):
    model: Verificaciones
    template_name = "includes/ver_verificaciones_auditoria.html"
    context_object_name: str


@login_required
def resumen_obleas(request):
    if request.htmx:
        logger.info("RENDERING HTMX!")
        data = []
        talleres = Talleres.objects.filter(activo__iexact=1)
        idtaller = request.GET.get("taller_id", None)
        logger.debug(request.GET)
        if idtaller:
            talleres = Talleres.objects.filter(idtaller__iexact=idtaller)

        for t in talleres:
            certs_by_taller = Certificadosasignadosportaller.objects.filter(
                idtaller=t.idtaller, disponible__iexact=1
            )

            cert_data = filter_vup_transporte(certs_by_taller)
            cert_data["taller"] = t.nombre

            data.append(cert_data)

        table = ObleasPorTallerTable(data)
        return render(request, "includes/table_view.html", {"table": table})

    initial_values = {
        "fecha_desde": "",
        "fecha_hasta": "",
        "taller_id": "",
    }

    form = ObleasPorTaller(initial=initial_values)
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


@method_decorator(login_required, name="dispatch")
class ResumenTransportePasajeros(CustomRTOView):
    # authentication_classes           = [authentication.TokenAuthentication]
    model = Verificaciones
    paginate_by = settings.PAGINATION
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


@method_decorator(login_required, name="dispatch")
class ResumenTransporteCarga(CustomRTOView):
    # authentication_classes = [authentication.TokenAuthentication]
    model = Verificaciones
    paginate_by = settings.PAGINATION
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


class PDFHabilitacion(PDFTemplateView):
    filename = "HABILITACION.pdf"
    template_name = "pdf/habilitacion.html"
    cmd_options = {"log-level": "info", "quiet": False, "enable-local-file-access": ""}

    def get_context_data(self, **kwargs):
        context = super(PDFHabilitacion, self).get_context_data(**kwargs)

        id_habilitacion = self.kwargs["idhabilitacion"]
        # dominio       = self.kwargs["dominio"]
        habilitacion = Habilitacion.objects.get(idhabilitacion=id_habilitacion)

        try:
            logger.debug(f"Checking usuario: {habilitacion}")
            user = User.objects.get(username=habilitacion.usuariodictamen).username
            username = f"{user.first_name} {user.lastname}"

        except Exception as e:
            logger.warning("User not found....")
            user = Usuarios.objects.get(usuario=habilitacion.usuariodictamen)
            username = f"{user.nombre} {user.apellido}"

        if habilitacion.tipopersona in "Jj":
            context["titular"] = habilitacion.razonsocialtitular
        else:
            context[
                "titular"
            ] = f"{habilitacion.nombretitular} {habilitacion.apellidotitular}"

        servicios = Serviciohab.objects.filter(idhabilitacion=id_habilitacion)

        descripciones = [s.idserviciostransportehab.descripcion for s in servicios]

        modificado = bool(habilitacion.modificado)
        logger.debug(f"Modificado => {modificado}")
        context["modificado"] = modificado

        cadena_id_servicio = "".join(
            [
                str(s.idserviciostransportehab.idserviciostransportehab).zfill(2)
                for s in servicios
            ]
        )

        # TODO Checkear que la fecha que uso esta bien

        barcode_path, barcode = build_barcode(
            id_habilitacion,
            str(habilitacion.fechahoradictamen)[0:10],
            habilitacion.dominio,
            cadena_id_servicio,
        )

        logger.debug(f"BARCODE => {barcode_path}")
        context["barcode_path"] = barcode_path
        context["barcode"] = barcode

        fechahora = habilitacion.fechahoracreacion
        date_str = f"Neuquén, {fechahora.day} de {MONTHS_DICT[fechahora.month]} de {fechahora.year}"
        context["date_str"] = date_str

        context["modelo"] = habilitacion.modelovehiculo
        context["dominio"] = habilitacion.dominio
        context["cccf"] = habilitacion.nrocertificadocccf

        context["tipo_servicio"] = descripciones

        context["username"] = username
        context["usersign"] = SIGN_DICT[habilitacion.usuariodictamen]

        return context


def carga_habilitacion(request, idhabilitacion=None, dominio=None, *args, **kwargs):
    if request.method == "POST":
        # if kwargs:
        #     idhabilitacion = kwargs.pop("idhabilitacion", None)
        #     dominio = kwargs.pop("dominio", None)

        # logger.debug(f"KWARGS => {dominio}-//-{idhabilitacion}")
        # if idhabilitacion and dominio:
        #     initial = handle_initial_hab(idhabilitacion, dominio)
        # else:
        #     initial = {}

        # logger.debug(f"INITIAL_DATA => {initial}")
        form = InspectionOrderForm(request.POST)

        if form.is_valid():
            try:
                hab = handle_save_hab(form.cleaned_data, request.user)

                logger.info(f"Habilitacion => {hab} SAVED!")
                success_message = "Form submitted successfully!"
                success_message_html = render_to_string(
                    "includes/success_message.html",
                    {"success_message": success_message},
                )
                return HttpResponse(success_message_html)
            except Exception as e:
                logger.error(e)
                error_message = "An error occurred: " + str(e)
                error_message_html = render_to_string(
                    "includes/error_message.html", {"error_message": error_message}
                )
                return HttpResponse(error_message_html)
            # Process the form data if needed
            # For example, you can access form.cleaned_data to get the validated data
            # Then redirect or render a success page
    else:
        if kwargs:
            idhabilitacion = kwargs.pop("idhabilitacion", None)
            dominio = kwargs.pop("dominio", None)

        logger.debug(f"KWARGS => {dominio}-//-{idhabilitacion}")
        if idhabilitacion and dominio:
            initial = handle_initial_hab(idhabilitacion, dominio)
        else:
            initial = {}

        logger.debug(f"INITIAL_DATA => {initial}")
        form = InspectionOrderForm(initial=initial)
        # form = InspectionOrderForm()

    return render(request, "includes/carga_habilitaciones.html", {"form": form})


def consulta_habilitaciones(request):
    if request.htmx:
        form = ConsultaDPTForm(request.GET)
        if form.is_valid():
            # Query the endpoint =>
            logger.debug(f"CLEANED DATA FROM FORM => {form.cleaned_data}")
            dpt_response = query_dpt(form.cleaned_data)
            logger.debug(f"RESPONSE FROM DPT => {dpt_response}")

            if isinstance(dpt_response, DPTResponse):
                table = ConsultaDPTTable(
                    [
                        dpt_response.dict(),
                    ]
                )
            elif isinstance(dpt_response, HabsResponse):
                table = ConsultaHabsTable(
                    [
                        dpt_response.dict(),
                    ]
                )

            return render(request, "includes/table_view.html", {"table": table})
    else:
        form = ConsultaDPTForm()

    return render(
        request,
        "includes/list_table.html",
        {"form": form, "render_url": "consulta_habilitaciones_finales"},
    )


def consulta_resumen_mensual(request, *args, **kwargs):
    if request.htmx:
        tipo_uso_user = get_tipo_uso_by_user(request)
        referer = request.META.get("HTTP_REFERER", None)
        logger.debug(f"ARGS PASSED TO ROUTING =>{tipo_uso_user}, {referer}")
        form = route_form(tipo_uso=tipo_uso_user, referer=referer)(request.GET)

        if form.is_valid():
            logger.debug(f"CLEANED DATA FROM FORM => {form.cleaned_data}")
            # Get the data, render HTML and cache the result
            uuid = get_resumen_data_mensual(form.cleaned_data, tipo_uso=tipo_uso_user)
            context = handle_resumen_context(uuid, **form.cleaned_data)
            cache_key_params = f"params__{uuid}"
            cache.set(cache_key_params, form.cleaned_data)

            return render(request, "pdf/resumen.html", context)
        else:
            logger.error(f"ERROR WHILE PARSING FORM => {form.errors}")
            raise ValidationError("Error while validating resumen FORM")
    else:
        tipo_uso = get_tipo_uso_by_user(request)
        today = datetime.today()
        prev = today - timedelta(weeks=8)

        tipo_uso_user = get_tipo_uso_by_user(request)
        initial_data = {
            "tipo_uso": tipo_uso,
            "fecha_desde": prev,
            "fecha_hasta": today,
            "id_taller": "",
        }

        tipo_uso_user = get_tipo_uso_by_user(request)
        referer = request.META.get("HTTP_REFERER", None)
        logger.debug(f"ARGS PASSED TO ROUTING =>{tipo_uso_user}, {referer}")
        form = route_form(tipo_uso=tipo_uso_user, referer=referer)(initial_data)

    return render(
        request,
        "includes/list_table.html",
        {"form": form, "render_url": "consulta_resumen_mensual"},
    )


class PDFResumenMensual(PDFTemplateView):
    filename = "resumen_mensual.pdf"
    template_name = "pdf/resumen_print.html"
    cmd_options = {
        "log-level": "info",
        "quiet": False,
        "enable-local-file-access": "",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # categorias = Verificaciones.values_list("id_categoria", flat=True).distinct()
        uuid = self.kwargs.get("uuid")
        logger.debug(f"UUID ===> {uuid}")

        params = cache.get(f"params__{uuid}")
        context = handle_resumen_context(uuid, **params)

        return context


def route_navigation(request, *args, **kwargs):
    referer = request.META.get("HTTP_REFERER", None)
    pass
