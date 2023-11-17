import os
from django.shortcuts import render
from django.views.generic.base import RedirectView, TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from datetime import date, datetime, timedelta

from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import (
    CccfAdjuntoscertificados,
    CccfCertificadoexcesos,
    CccfCertificados,
)
from .tables import (
    CCCFTable,
)
from .helpers import (
    convert_date,
    generate_cccf_key,
    handle_context,
    AuxData,
)

from .forms import (
    CustomRTOForm,
)  # Import the form you created

from .views import CustomRTOView, ChangeModelView, IndexView

from .logging import configure_logger, print_stack
from .name_schemas import *

LOG_FILE = os.environ["LOG_FILE"]
logger = configure_logger(LOG_FILE)


class CCCFView(IndexView):
    urls = {
        "cccf_list": "Listar CCCF",
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

        certificado.idestado = 3
        certificado.fechaanulacion = datetime.today()

        if observaciones:
            certificado.observaciones = observaciones

        certificado.save()
        return True

    except Exception as e:
        logger.error(f"UPDATING FAILED => {e}")
        return False


class AnularCCCF(ChangeModelView):
    model = CccfCertificados
    msg_estado = "Fue anulado"
    operation = anular_certificado
    id_param = "nrocertificado"
    delete_msg = "El CCCF Numero:"
    table_view = "cccf_list"
