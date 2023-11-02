from django.contrib import admin
from django.urls import path, include

# TODO Check this kind of errors
import rto_consultas_rn.views as views_RN

urlpatterns = [
    path("dvr", views_RN.dvr_view, name="dvr"),
    path("sec_transporte",
         views.secretaria_transporte_view,
         name="sec_transporte"),
    path(
        "ververificacion/<int:idverificacion>/<int:idtaller>",
        views_RN.VerVerificacion_RN.as_view(),
        name="ver_verificacion",
    ),
    path("verificaciones_rn",
         views_RN.ListVerificacionesView_RN.as_view(),
         name="verificaciones_rn"),
]
