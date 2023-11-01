from django.contrib import admin
from django.urls import path, include
from . import views

urlpatters = [
    path("/verificaciones_rn", views.ListVerificacionesView.as_view(), name="verificaciones_rn"),
    path(
        "ververificacion/<int:idverificacion>/<int:idtaller>",
        views.VerVerificacion.as_view(),
        name="ver_verificacion",
    ),
]
