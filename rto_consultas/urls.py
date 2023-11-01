"""rto_consultas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import rto_consultas.views as views

urlpatterns = [
    path("accounts/login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("admin/", admin.site.urls),
    path("", views.index, name="home"),
    path("", views.index, name="index"),
]

urlpatterns += [
    path(
        "ansv",
        views.ansv_view,
        name="ansv",
    ),
    path(
        "dpt",
        views.dpt_view,
        name="dpt",
    ),
]

urlpatterns += [
    # path("accounts/", include("django.contrib.auth.urls")),
    path(
        "verificaciones/resumen?_export=csv",
        views.ListarVerificacionesTotales.as_view(),
        name="descargar_resumen",
    ),
    path(
        "verificaciones/resumen",
        views.ListarVerificacionesTotales.as_view(),
        name="verificaciones_resumen",
    ),
    path("habilitaciones/", views.ListHabilitaciones.as_view(), name="habilitaciones"),
    path(
        "verificaciones/", views.ListVerificacionesView.as_view(), name="verificaciones"
    ),
    path(
        "certs_assignados/",
        views.ListCertificadosAssignView.as_view(),
        name="certs_asignados",
    ),
    path("certificados/", views.ListCertificadosView.as_view(), name="certificados"),
    path("vehiculos/", views.ListVehiculosView.as_view(), name="vehiculos"),
    path("cargaobleas/", views.CargaObleas.as_view(), name="carga_obleas"),
    path("resumenobleas/", views.resumen_obleas, name="resumen_obleas"),
    path(
        "cargahabilitacion/",
        views.carga_habilitacion,
        name="carga_habilitacion",
    ),
    path(
        "verhabilitacion/<int:idhabilitacion>/<str:dominio>",
        views.VerHabilitacion.as_view(),
        name="ver_habilitacion",
    ),
    path(
        "pdf_habilitacion/<int:idhabilitacion>",
        views.PDFHabilitacion.as_view(),
        name="pdfhabilitacion",
    ),
    path(
        "ververificacion/<int:idverificacion>/<int:idtaller>",
        views.VerVerificacion.as_view(),
        name="ver_verificacion",
    ),

    path(
        "consulta_dpt",
        views.consulta_habilitaciones,
        name="consulta_habilitaciones",
    ),
    # path("", include("admin_soft.urls"), name=admin),
]
# urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]

urlpatterns += [
    path("cantverificaciones", views.verificaciones_anuales),
    path("obleasportaller", views.resumen_obleas),
]

urlpatterns += [
    path(
        "resumen/transporte",
        views.ResumenTransportePasajeros.as_view(),
        name="resumen_dpt_pasajeros",
    ),
    path(
        "resumen/carga",
        views.ResumenTransporteCarga.as_view(),
        name="resumen_dpt_carga",
    ),
]
urlpatterns += [path("", include("rto_consultas_rn.urls")),]
