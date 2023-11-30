from django.contrib import admin
from django.urls import path, include

# TODO Check this kind of errors
import rto_consultas_rn.views as views_RN

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
    path(
        "excepciones_rn_form/",
        views_RN.RenderExcepcionesForm_RN.as_view(),
        name="excepciones_rn_form",
    ),
]
