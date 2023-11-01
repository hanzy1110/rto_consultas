from django.contrib import admin
from django.urls import path, include

# TODO Check this kind of errors
import rto_consultas_rn.views as views

urlpatterns = [
    path("dvr", views.dvr_view, name="dvr"),
    path("sec_transporte",
         views.secretaria_transporte_view,
         name="sec_transporte"),
    path(
        "ververificacion/<int:idverificacion>/<int:idtaller>",
        views.VerVerificacion.as_view(),
        name="ver_verificacion",
    ),
    path("verificaciones_rn",
         views.ListVerificacionesView.as_view(),
         name="verificaciones_rn"),
]
