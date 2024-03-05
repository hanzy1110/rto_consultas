from logging import disable
import os
from django.db.models import Model, Prefetch
from django.shortcuts import render
from django.views.generic.detail import DetailView
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
from django.http import HttpResponse
from django.template.loader import render_to_string

from django.contrib.auth.models import User

from wkhtmltopdf.views import PDFTemplateView

from datetime import date
from django.conf import settings

from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django_tables2.export.export import TableExport
from django.contrib import messages

from admin_soft.forms import LoginForm

from autocomplete import HTMXAutoComplete

from .models import (
    Adjuntos,
    Excepcion,
    Localidades,
    Personas,
    Prorroga,
    Provincias,
    Talleres,
    Usuarios,
    Verificaciones,
    Certificadosasignadosportaller,
    Vehiculos,
    Oits,
    Certificados,
    Categorias,
    Verificacionesdefectos,
    Verificacionespdf,
)
from rto_consultas_rn.models import Estados, Tipousovehiculo
from rto_consultas_rn.models import Talleres as TalleresRN

from rto_consultas_rn.tables import (
    ExcepcionesTable_RN,
    ObleasPorTallerTable_RN,
    OitsTable_RN,
    ProrrogasTable_RN,
    ResumenTransporteCargaTable,
    ResumenTransporteTable,
    VerificacionesTables,
    ObleasPorTallerTable,
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
    handle_save_excepcion,
    handle_initial_excepcion,
    handle_update_excepcion,
    get_queryset_from_user,
)

from rto_consultas.forms import (
    CustomRTOForm,
)  # Import the form you created

from rto_consultas_rn.forms import ObleasPorTaller, ExcepcionesFirstForm

from rto_consultas.logging import configure_logger, print_stack
from rto_consultas.views import IndexView
from rto_consultas.name_schemas import USER_GROUPS

LOG_FILE = os.environ["LOG_FILE"]
logger = configure_logger(LOG_FILE)


@login_required
def rn_view(request):
    template_name = "pages/RN/index_rn.html"
    return render(request, template_name, {"segment": "index"})


class DVRView(IndexView):
    urls = {
        "verificaciones_rn": "Verificaciones",
        "carga_obleas_rn": "Carga Obleas",
        "resumen_obleas_rn": "Consulta Disponibilidad Obleas",
        "excepciones_rn": "Consulta Excepciones",
        "carga_excepciones_rn": "Carga Excepciones",
        "prorrogas_rn": "Consulta Prorrogas",
    }


class SecTranspView(IndexView):
    urls = {
        "oits": "Consulta Órdenes de Inspección",
        "verificaciones_rn": "Verificaciones",
    }


class CustomRTOView_RN(ExportMixin, SingleTableView, LoginRequiredMixin):
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
        if page:
            # Handle pagination...
            self.table_data = queryset
            self.get_table()

        return queryset

    def get_context_data(self, **kwargs):
        # logger.debug("HANDLING CONTEXT...")
        context = super().get_context_data(**kwargs)
        user = self.request.user
        try:
            self.user_group = next(
                filter(lambda x: user.groups.filter(name=x).exists(), USER_GROUPS)
            )
        except Exception as e:
            logger.warn(f"User with no group {self.request.user.username} ===> {e}")
            self.user_group = None

        logger.info(self.user_group)

        context = handle_context(context, self)
        logger.debug("CONTEXT HANDLED...")
        return context

    def get_template_names(self):
        if self.request.htmx:
            # logger.debug("RIO NEGRO HTMX REQUEST!!")
            # logger.info(f"CURRENT STACK =>{print_stack()}")
            return [self.partial_template]
        return [self.template_name]


@method_decorator(login_required, name="dispatch")
class ListVerificacionesView_RN(CustomRTOView_RN):
    # authentication_classes = [authentication.TokenAuthentication]
    model = Verificaciones
    paginate_by = settings.PAGINATION
    template_name = "includes/list_table_RN.html"
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
        render_url="verificaciones_rn",
        render_form="verificaciones_form_rn",
    )

    def get_queryset(self):
        logger.info("CALCULATE QUERYSET...")
        page = self.request.GET.copy().get("page", None)

        queryset = super().get_queryset()
        if isinstance(queryset, list):
            queryset = list(reversed(queryset))
        else:
            queryset = queryset.order_by("-idverificacion")
            queryset = queryset.order_by("-fecha")

        logger.info("QUERYSET DONE...")

        if page:
            # Handle pagination...
            self.table_data = queryset
            self.get_table()
        queryset = get_queryset_from_user(queryset, self.request)
        return queryset

    # def get_queryset(self):
    #     logger.info("CALCULATE QUERYSET...")
    #     queryset = super().get_queryset()
    #     if isinstance(queryset, list):
    #         pass
    #         queryset = list(reversed(queryset))
    #     else:
    #         queryset = queryset.order_by("-idverificacion")
    #     logger.info("QUERYSET DONE...")
    #     return queryset


@method_decorator(login_required, name="dispatch")
class RenderVerificacionForm_RN(TemplateView):
    template_name = "includes/form_render.html"

    aux_data = AuxData(
        query_fields=[
            "dominiovehiculo",
            "nrocertificado",
            "fecha_desde",
            "fecha_hasta",
            "dni",
            "nro_dni",
        ],
        form_fields={
            "idestado": ("descripcion", Estados),
            "idtipouso": ("descripcion", Tipousovehiculo),
            "idtaller": ("nombre", TalleresRN),
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
        render_url="verificaciones_rn",
    )

    form_class = CustomRTOForm
    model = Verificaciones

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        try:
            self.user_group = next(
                filter(lambda x: user.groups.filter(name=x).exists(), USER_GROUPS)
            )
        except Exception as e:
            logger.warn(f"User with no group {self.request.user.username} ===> {e}")
            self.user_group = None

        logger.info(self.user_group)

        context = handle_context(context, self)
        return context


@method_decorator(login_required, name="dispatch")
class VerVerificacion_RN(DetailView, LoginRequiredMixin):
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

        adjuntos = [generate_key(a, bucket_name="rto-rn-files") for a in adjuntos]
        context["certificado"] = cert[0]
        context["url_certificado"] = generate_key_certificado(
            pdf_certificado, bucket_name="rto-rn-files"
        )
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


@method_decorator(login_required, name="dispatch")
class ListOits_RN(CustomRTOView_RN):
    # authentication_classes           = [authentication.TokenAuthentication]
    model = Oits
    template_name = "includes/list_table.html"
    paginate_by = settings.PAGINATION
    context_object_name = "Oits"
    table_class = OitsTable_RN
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
        render_url="oits",
        render_form="oits_form",
    )

    def get_queryset(self):
        logger.info("CALCULATE QUERYSET...")
        queryset = super().get_queryset()
        if isinstance(queryset, list):
            queryset = list(reversed(queryset))
        else:
            queryset = queryset.order_by("-numero")
        logger.info("QUERYSET DONE...")
        return queryset


@method_decorator(login_required, name="dispatch")
class RenderOitsForm_RN(TemplateView):
    template_name = "includes/form_render.html"

    aux_data = AuxData(
        query_fields=[
            "dominio",
            "numero",
            "fecha_desde",
            "fecha_hasta",
        ],
        form_fields={},
        parsed_names={
            "dominio": "Dominio Vehiculo",
            "fecha_desde": "Fecha Desde",
            "fecha_hasta": "Fecha Hasta",
        },
        ids={"dominiovehiculo": "#txtDominio"},
        types={
            "dominio": "text",
            "fecha_desde": "date",
            "fecha_hasta": "date",
        },
        render_url="oits",
        fecha_field="fecha",
    )

    form_class = CustomRTOForm
    model = Oits

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        try:
            self.user_group = next(
                filter(lambda x: user.groups.filter(name=x).exists(), USER_GROUPS)
            )
        except Exception as e:
            logger.warn(f"User with no group {self.request.user.username} ===> {e}")
            self.user_group = None

        context = handle_context(context, self)
        return context


@method_decorator(login_required, name="dispatch")
class ListExcepciones_RN(CustomRTOView_RN):
    # authentication_classes           = [authentication.TokenAuthentication]
    model = Excepcion
    template_name = "includes/list_table.html"
    paginate_by = settings.PAGINATION
    context_object_name = "Oits"
    table_class = ExcepcionesTable_RN
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
            "dominio": "#txtDominio",
        },
        types={
            "dominio": "text",
        },
        render_url="excepciones_rn",
        render_form="excepciones_rn_form",
    )

    def get_queryset(self):
        logger.info("CALCULATE QUERYSET...")
        queryset = super().get_queryset()
        if isinstance(queryset, list):
            queryset = list(reversed(queryset))
        else:
            queryset = queryset.order_by("-fecha")
        logger.info("QUERYSET DONE...")
        return queryset


# @method_decorator(login_required, name="dispatch")
# class RenderExcepcionesForm_RN(TemplateView):
#     template_name = "includes/form_render.html"

#     aux_data = AuxData(
#         query_fields=[
#             "dominio",
#             "idtipouso",
#             "fecha_desde",
#             "fecha_hasta",
#         ],
#         form_fields={
#             "idtaller": ("nombre", Talleres),
#         },
#         parsed_names={
#             "dominio": "Dominio Vehiculo",
#             "idtaller": "Planta",
#             "fecha_desde": "Fecha Desde",
#             "fecha_hasta": "Fecha Hasta",
#         },
#         ids={"dominiovehiculo": "#txtDominio"},
#         types={
#             "dominio": "text",
#             "fecha_desde": "date",
#             "fecha_hasta": "date",
#         },
#         render_url="excepciones_rn",
#         fecha_field="fecha",
#     )

#     form_class = CustomRTOForm
#     model = Excepcion

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.request.user
#         try:
#             self.user_group = next(
#                 filter(lambda x: user.groups.filter(name=x).exists(), USER_GROUPS)
#             )
#         except Exception as e:
#             logger.warn(f"User with no group {self.request.user.username} ===> {e}")
#             self.user_group = None

#         context = handle_context(context, self)
#         return context


@method_decorator(login_required, name="dispatch")
class ListProrrogas_RN(CustomRTOView_RN):
    # authentication_classes           = [authentication.TokenAuthentication]
    model = Prorroga
    template_name = "includes/list_table.html"
    paginate_by = settings.PAGINATION
    context_object_name = "Oits"
    table_class = ProrrogasTable_RN
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
            "dominio": "#txtDominio",
        },
        types={
            "dominio": "text",
        },
        render_url="prorrogas_rn",
        render_form="prorrogas_rn_form",
    )

    def get_queryset(self):
        logger.info("CALCULATE QUERYSET...")
        queryset = super().get_queryset()
        if isinstance(queryset, list):
            queryset = list(reversed(queryset))
        else:
            queryset = queryset.order_by("-fechahoracreacion")
        logger.info("QUERYSET DONE...")
        return queryset


@method_decorator(login_required, name="dispatch")
class RenderExcepcionesForm_RN(TemplateView):
    template_name = "includes/form_render.html"

    aux_data = AuxData(
        query_fields=[
            "dominio",
            "fecha_desde",
            "fecha_hasta",
        ],
        form_fields={
            "idtaller": ("nombre", Talleres),
        },
        parsed_names={
            "dominio": "Dominio Vehiculo",
            "idtaller": "Planta",
            "fecha_desde": "Fecha Desde",
            "fecha_hasta": "Fecha Hasta",
        },
        ids={"dominiovehiculo": "#txtDominio"},
        types={
            "dominio": "text",
            "fecha_desde": "date",
            "fecha_hasta": "date",
        },
        render_url="excepciones_rn",
        fecha_field="fechahoracreacion",
    )

    form_class = CustomRTOForm
    model = Excepcion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        try:
            self.user_group = next(
                filter(lambda x: user.groups.filter(name=x).exists(), USER_GROUPS)
            )
        except Exception as e:
            logger.warn(f"User with no group {self.request.user.username} ===> {e}")
            self.user_group = None

        context = handle_context(context, self)
        return context


@method_decorator(login_required, name="dispatch")
class VerHabilitacion_RN(DetailView, LoginRequiredMixin):
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


class ResumenObleas_RN(CustomRTOView_RN, LoginRequiredMixin):
    model = Certificadosasignadosportaller
    paginate_by = settings.PAGINATION
    template_name = "includes/list_table.html"
    context_object_name = "Certificados Asignados por taller"
    table_class = ObleasPorTallerTable
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
        render_url="obleas_por_taller_rn",
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
        table = ObleasPorTallerTable(data)
        context["table"] = table

        return context


class CargaObleas(CustomRTOView_RN):
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
        render_url="carga_obleas_rn",
    )


@login_required
def resumen_obleas_rn(request):
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

            # cert_data = filter_vup_transporte(certs_by_taller)
            cert_data = {"cant": len(certs_by_taller), "taller": t.nombre}

            data.append(cert_data)

        table = ObleasPorTallerTable_RN(data)
        return render(request, "includes/table_view.html", {"table": table})

    initial_values = {
        "fecha_desde": "",
        "fecha_hasta": "",
        "taller_id": "",
    }

    form = ObleasPorTaller(initial=initial_values)
    return render(
        request,
        "includes/consulta_obleas.html",
        {"form": form, "resumen_obleas_url": "resumen_obleas_rn"},
    )


def carga_excepcion(request, dominio=None, *args, **kwargs):
    logger.info(f"request method = {request.method}, htmx? {request.htmx}")
    if request.method == "POST":
        form = ExcepcionesFirstForm(request.POST)
        # form_informes = InformesForm(request.POST)

        if form.is_valid():
            try:
                cccf = handle_save_excepcion(
                    form.cleaned_data,
                    request.user,
                )

                logger.info(f"CCCF => {cccf} SAVED!")

                success_message = "Form submitted successfully!"
                success_message_html = render_to_string(
                    "carga_cccf/estado_success.html",
                    {"success_message": success_message},
                )

                res = HttpResponse(success_message_html)
                res.headers["HX-Trigger"] = "reloadEstadoSuccess"
                return res

            except IndentationError as e:
                logger.error(e)
                error_message = "An error occurred: " + str(e)
                error_message_html = render_to_string(
                    "carga_cccf/estado_error.html", {"error_message": error_message}
                )
                res = HttpResponse(error_message_html)
                res.headers["HX-Trigger"] = "reloadEstadoError"
                return res
        else:
            logger.error(f"Validation Error => {form.errors}")
            assert False

    else:
        if kwargs:
            dominio = kwargs.pop("dominio", None)

        # logger.debug(f"KWARGS => {dominio}-//-{idhabilitacion}")
        if dominio:
            initial = handle_initial_excepcion(dominio)
        else:
            initial = {}

        if settings.DEBUG:
            logger.warn("USING DEBUG DATA!!!")
            initial = handle_initial_excepcion("AE-512-IN")

        logger.debug(f"INITIAL_DATA => {initial}")
        form = ExcepcionesFirstForm(initial=initial)
        # form_informes = InformesForm(initial=initial)

        return render(
            request,
            "includes/carga_excepcion.html",
            {
                "form": form,
                "dominio": "avb",
                "post_link": "dictaminar_excepcion",
            },
        )


def excepciones_estado_success(request, *args, **kwargs):
    stored_messages = messages.get_messages(request)
    context = {"messages": stored_messages}
    return render(
        request, template_name="msgs/estado_success.html", context=context
    )


def excepciones_estado_error(request, *args, **kwargs):
    stored_messages = messages.get_messages(request)
    context = {"messages": stored_messages}
    return render(request, template_name="msgs/estado_error.html", context=context)


def dictaminar_excepcion(request, dominio=None, *args, **kwargs):
    if request.method == "POST":
        # form = ExcepcionesFirstForm(request.POST, disable_edition=False)
        # form_informes = InformesForm(request.POST)

        if True:
            try:
                exc = handle_update_excepcion(
                    # form.cleaned_data,
                    request.POST,
                    dominio,
                    request.user,
                )

                logger.info(f"exc => {exc} SAVED!")

                success_message = "Form submitted successfully!"
                success_message_html = render_to_string(
                    "msgs/estado_success.html",
                    {"success_message": success_message},
                )

                res = HttpResponse(success_message_html)
                res.headers["HX-Trigger"] = "reloadEstadoSuccess"
                return res

            except IndentationError as e:
                logger.error(e)
                error_message = "An error occurred: " + str(e)
                error_message_html = render_to_string(
                    "msgs/estado_error.html", {"error_message": error_message}
                )
                res = HttpResponse(error_message_html)
                res.headers["HX-Trigger"] = "reloadEstadoError"
                return res
        else:
            logger.error(f"Validation Error => {form.errors}")
            assert False
    else:
        logger.info(f"request method = {request.method}, htmx? {request.htmx}")
        if kwargs:
            dominio = kwargs.pop("dominio", None)

        # logger.debug(f"KWARGS => {dominio}-//-{idhabilitacion}")
        if dominio:
            initial = handle_initial_excepcion(dominio)
        else:
            initial = {}

        if settings.DEBUG:
            logger.warn("USING DEBUG DATA!!!")
            initial = handle_initial_excepcion("AE-512-IN")

        logger.debug(f"INITIAL_DATA => {initial}")
        form = ExcepcionesFirstForm(disable_edition=True, initial=initial)
        # form_informes = InformesForm(initial=initial)

        return render(
            request,
            "includes/carga_excepcion.html",
            {"form": form, "dominio": dominio, "post_link": "dictaminar_excepcion"},
        )
