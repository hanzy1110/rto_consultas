import os
from django.shortcuts import HttpResponse, render
from django.template.loader import render_to_string
from django.views.generic.base import RedirectView, TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.core.cache import cache
from django.contrib import messages

from django.core.files.storage import FileSystemStorage

from datetime import date, datetime, timedelta

from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django_tables2 import SingleTableView

from .models import (
    CccfAdjuntoscertificados,
    CccfCertificadoexcesos,
    CccfCertificados,
)
from .tables import (
    CCCFExcesosTable,
    CCCFTable,
)
from .helpers import (
    allow_keys,
    convert_date,
    generate_cccf_key,
    handle_context,
    AuxData,
    handle_initial_cccf,
    handle_save_cccf,
    handle_upload_file,
)

from .forms import (
    CCCFForm,
    CustomRTOForm,
    InformesForm,
)  # Import the form you created

from .views import CustomRTOView, ChangeModelView, IndexView

from .logging import configure_logger, print_stack
from .name_schemas import *

LOG_FILE = os.environ["LOG_FILE"]
logger = configure_logger(LOG_FILE)


class CCCFView(IndexView):
    urls = {
        "cccf_list": "Listar CCCF",
        "cccf_carga": "Cargar CCCF",
        # "carga_certificados": "Cargar CCCF",
    }


@method_decorator(login_required, name="dispatch")
class ListCCCFView(CustomRTOView):
    # authentication_classes = [authentication.TokenAuthentication]
    model = CccfCertificados
    paginate_by = settings.PAGINATION
    template_name = "includes/list_table.html"
    context_object_name = "CCCF"
    table_class = CCCFTable
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
        render_url="cccf_list",
        render_form="cccf_form",
        fecha_field="fechahoracarga",
    )

    def get_queryset(self):
        logger.info("CALCULATE QUERYSET...")
        queryset = super().get_queryset()
        if isinstance(queryset, list):
            queryset = list(reversed(queryset))
        else:
            # queryset = queryset.order_by("-idverificacion")
            queryset = queryset.order_by(f"-{self.aux_data.fecha_field}")
        logger.info("QUERYSET DONE...")
        return queryset


@method_decorator(login_required, name="dispatch")
class CCCFRenderForm(TemplateView):
    template_name = "includes/form_render.html"

    aux_data = AuxData(
        query_fields=[
            "dominio",
            "nrocertificado",
            "fecha_desde",
            "fecha_hasta",
        ],
        form_fields={
            # "idestado": ("descripcion", Estados),
            # "idtipouso": ("descripcion", Tipousovehiculo),
            # "idtaller": ("nombre", Talleres),
            # "anulado": (None, None),
        },
        parsed_names={
            "dominiovehiculo": "Dominio",
            "nrocertificado": "Nro. Certificado",
            "fecha_desde": "Fecha Desde",
            "fecha_hasta": "Fecha Hasta",
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
        render_url="cccf_list",
        fecha_field="fechahoracarga",
    )

    form_class = CustomRTOForm
    model = CccfCertificados

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = handle_context(context, self)
        return context


@method_decorator(login_required, name="dispatch")
class VerCCCF(DetailView, LoginRequiredMixin):
    model: CccfCertificados
    template_name = "includes/ver_cccf.html"
    context_object_name = "certificado"
    aux_data: AuxData

    def get_object(self):
        query_params = self.request.GET.copy()
        nrocertificado = self.kwargs["nrocertificado"]

        cccf = CccfCertificados.objects.select_related("idempresa", "idtaller").get(
            nrocertificado__iexact=nrocertificado
        )
        logger.debug(cccf)
        self.cccf = cccf
        return cccf

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cccf_excesos"] = CccfCertificadoexcesos.objects.filter(
            idcertificado=self.cccf.idcertificado
        )
        cccf_adjuntos = CccfAdjuntoscertificados.objects.filter(
            idcertificado=self.cccf.idcertificado
        )

        # cccf_urls = [
        #     generate_cccf_key(ad, self.cccf.idtaller_id) for ad in cccf_adjuntos
        # ]
        # TODO No tocar hasta no tener los archivos trasladados

        cccf_urls = ["" for _ in cccf_adjuntos]
        context["ADJUNTOS"] = list(zip(cccf_adjuntos, cccf_urls))

        return context


def anular_certificado(certificado, observaciones=None):
    # $sqlUpCert = "UPDATE cccf_certificados SET idEstado = 3, FechaAnulacion='".date("Y-m-d")."',ObservacionesAnulacion='$observaciones' WHERE idCertificado = $idCertifcado "
    #                     . " AND idTaller = $idTaller";

    try:
        logger.info("ANULANDO CERTIFICADO!")
        # certificado.idestado = 3
        # certificado.fechaanulacion = datetime.today()

        # if observaciones:
        #     certificado.observaciones = observaciones

        # certificado.save()
        return True

    except Exception as e:
        logger.error(f"UPDATING FAILED => {e}")
        return False


def get_cccf_modal(request, *args, **kwargs):
    context = {}
    context["nrocertificado"] = kwargs.get("nrocertificado", None)
    context["dominio"] = kwargs.get("dominio", None)

    return render(request, template_name="tables/confirm_delete.html", context=context)


def get_cccf_modal_excesos(request, *args, **kwargs):
    context = {}
    context["nrocertificado"] = kwargs.get("nrocertificado", None)
    context["dominio"] = kwargs.get("dominio", None)

    return render(request, template_name="carga_cccf/modal_cccf.html", context=context)


class AnularCCCF(ChangeModelView):
    model = CccfCertificados
    msg_estado = "Fue anulado"
    operation = anular_certificado
    id_param = "nrocertificado"
    delete_msg = "El CCCF Numero:"
    table_view = "cccf_list"


def carga_cccf(request, nrocertificado=None, dominio=None, *args, **kwargs):
    logger.info(f"request method = {request.method}, htmx? {request.htmx}")
    if request.method == "POST":
        form = CCCFForm(request.POST)
        # form_informes = InformesForm(request.POST)

        logger.info(f"form valid? {form.is_valid()}")
        if form.is_valid():
            try:
                files = request.FILES.get("cccf_files")
                logger.debug(f"FILES => {dir(files)}")
                logger.debug(f"FILES => {files}")
                handle_upload_file(files, s3_prefix="ADJUNTOS_CCCF")
                cccf = handle_save_cccf(
                    form.cleaned_data,
                    # form_informes.cleaned_data,
                    request.user,
                    request.FILES["cccf_files"],
                )
                logger.info(f"CCCF => {cccf} SAVED!")
                success_message = "Form submitted successfully!"
                success_message_html = render_to_string(
                    "includes/success_message.html",
                    {"success_message": success_message},
                )
                return HttpResponse(success_message_html)
            except ValueError as e:
                logger.error(e)
                error_message = "An error occurred: " + str(e)
                error_message_html = render_to_string(
                    "includes/error_message.html", {"error_message": error_message}
                )
                return HttpResponse(error_message_html)
        else:
            logger.error(f"Validation Error => {form.errors}")
            assert False

    else:
        if kwargs:
            nrocertificado = kwargs.pop("nrocertificado", None)
            dominio = kwargs.pop("dominio", None)

        # logger.debug(f"KWARGS => {dominio}-//-{idhabilitacion}")
        if nrocertificado and dominio:
            initial = handle_initial_cccf(nrocertificado, dominio)
        else:
            initial = {}

        logger.debug(f"INITIAL_DATA => {initial}")
        form = CCCFForm(initial=initial)
        form_informes = InformesForm(initial=initial)

        return render(
            request,
            "includes/carga_cccf.html",
            {"form": form, "form_informes": form_informes},
        )


def add_cccf_exceso(request, *args, **kwargs):
    nrocertificado = kwargs.pop("nrocertificado", None)
    nrocertificado = request.GET.get("nrocertificado", None)

    logger.debug(f"REQUEST PARAMS => {request.GET}")

    if nrocertificado:
        nrocertificado = int(nrocertificado)
        # cccf = CccfCertificados.objects.get(nrocertificado__iexact=nrocertificado)
        # count_ = CccfCertificadoexcesos.objects.filter(idcertificado=cccf).count()
        cache_key = f"excesos_{nrocertificado if nrocertificado else 0}"
        prev_data = cache.get(cache_key, [])

        data = {}
        data["fecha"] = request.GET.get("fecha", None)
        data["numero"] = len(prev_data) - 1 if len(prev_data) > 0 else 1
        data["hora"] = request.GET.get("hora", None)
        data["velocidadsobrepaso"] = request.GET.get("velocidadsobrepaso", None)
        data["tiempovelocidadexceso"] = request.GET.get("tiempovelocidadexceso", None)
        data["nrocertificado"] = nrocertificado

        prev_data.append(data)
        cache.set(cache_key, prev_data)
        logger.debug(f"DATA =====> {data}")
        logger.debug(f"PREV_DATA =====> {prev_data}")
        messages.success(request, f"Exceso de Velocidad Añadido")

        # try:
        #     new_exceso = CccfCertificadoexcesos(**data)
        #     new_exceso.save()
        #     messages.success(request, f"Exceso de Velocidad Añadido")
        # except Exception as e:
        #     logger.error(e)
        #     messages.error(request, "Error al cargar exceso")

    else:
        messages.error(request, "Cargue Nro. de Certificado")

    context = {
        "messages": [m.message for m in messages.get_messages(request)][-1],
    }
    res = HttpResponse(
        render_to_string(template_name="tables/table_messages.html", context=context)
    )
    res.headers["HX-Trigger"] = "reloadTableExcesos"

    return res


def consulta_excesos(request, *args, **kwargs):
    if request.htmx:
        nrocertificado = kwargs.pop("nrocertificado", None)
        nrocertificado = request.GET.get("nrocertificado", None)
        logger.debug(f"CCCF NRO : {type(nrocertificado)} => { nrocertificado }")

        if nrocertificado:
            nrocertificado = int(nrocertificado)
            # cccf = CccfCertificados.objects.get(nrocertificado__iexact=nrocertificado)
            # count_ = CccfCertificadoexcesos.objects.filter(idcertificado=cccf).count()
        cache_key = f"excesos_{nrocertificado if nrocertificado else 0}"
        prev_data = cache.get(cache_key, [])
        logger.info(f"PREV DATA = {prev_data}")
        if prev_data:
            table = CCCFExcesosTable(
                list(
                    map(
                        lambda x: allow_keys(
                            x,
                            [
                                "numero",
                                "fecha",
                                "hora",
                                "velocidadsobrepaso",
                                "tiempovelocidadexceso",
                            ],
                        ),
                        prev_data,
                    )
                )
            )
        else:
            logger.warn("CACHE MISS ON CCCF")
            table = CCCFExcesosTable([])
        return render(request, "includes/table_view.html", {"table": table})
