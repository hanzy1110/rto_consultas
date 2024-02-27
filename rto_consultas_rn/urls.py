from django.contrib import admin
from django.urls import path, include

# TODO Check this kind of errors
import rto_consultas_rn.views as views_RN
from rto_consultas.helpers import TipoUsoAutocomplete, TallerAutocomplete_RN, LocalidadesAutocomplete_RN

urlpatterns = [
    path("dvr", views_RN.DVRView.as_view(), name="dvr"),
    path("sec_transporte", views_RN.SecTranspView.as_view(), name="sec_transporte"),
    path(
        "oits_form/",
        views_RN.RenderOitsForm_RN.as_view(),
        name="oits_form",
    ),
    path(
        "obleas_por_taller_rn/",
        views_RN.ResumenObleas_RN.as_view(),
        name="obleas_por_taller_rn",
    ),
    path(
        "prorrogas_rn",
        views_RN.ListProrrogas_RN.as_view(),
        name="prorrogas_rn",
    ),
    path(
        "prorrogas_rn_form",
        views_RN.ListProrrogas_RN.as_view(),
        name="prorrogas_rn_form",
    ),
    path(
        "oits/",
        views_RN.ListOits_RN.as_view(),
        name="oits",
    ),
    path(
        "verificaciones_form_rn/",
        views_RN.RenderVerificacionForm_RN.as_view(),
        name="verificaciones_form_rn",
    ),
    path(
        "ververificacion_rn/<int:idverificacion>/<int:idtaller>",
        views_RN.VerVerificacion_RN.as_view(),
        name="ver_verificacion_rn",
    ),
    path(
        "verificaciones_rn",
        views_RN.ListVerificacionesView_RN.as_view(),
        name="verificaciones_rn",
    ),
    path(
        "excepciones_rn/",
        views_RN.ListExcepciones_RN.as_view(),
        name="excepciones_rn",
    ),
    path("cargaobleas_rn/", views_RN.CargaObleas.as_view(), name="carga_obleas_rn"),
    path(
        "excepciones_rn_form/",
        views_RN.RenderExcepcionesForm_RN.as_view(),
        name="excepciones_rn_form",
    ),

    path("dictaminar_excepcion", views_RN.carga_excepcion, name="dictaminar_excepcion"),
    path("carga_excepciones_rn", views_RN.dictaminar_excepcion, name="carga_excepciones_rn"),
    path("excepciones_estado_success", views_RN.excepciones_estado_success, name="excepciones_estado_success"),
    path("excepciones_estado_error", views_RN.excepciones_estado_error, name="excepciones_estado_error"),
    path("resumen_obleas_rn", views_RN.resumen_obleas_rn, name="resumen_obleas_rn"),
    path("idtipouso", TipoUsoAutocomplete.as_view(), name="idtipouso"),
    path("talleres_rn", TallerAutocomplete_RN.as_view(), name="talleres_rn"),
    path("localidades_rn", LocalidadesAutocomplete_RN.as_view(), name="localidades_rn"),

]
