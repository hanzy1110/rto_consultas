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
from django.conf import settings
from django.urls import path, include
from django.views.static import serve
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rto_consultas.cccf_views import (
    AnularCCCF,
    CCCFView,
    CargaPrecinto,
    CccfTalleresList,
    ListCCCFView,
    CCCFRenderForm,
    VerCCCF,
    PDFCccf,
    add_cccf_exceso,
    carga_cccf,
    cccf_estado_error,
    cccf_estado_success,
    consulta_excesos,
    dar_de_baja_taller_cccf,
    dar_de_baja_taller_cccf_confirm,
    editar_cccf_taller,
    get_cccf_modal,
    get_cccf_modal_excesos,
    taller_edit_failure,
    taller_edit_success,
    ver_cccf_usuarios,
)

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
        "seg_vial_auditoria/",
        views.SVViewAuditoria.as_view(),
        name="seg_vial_auditoria",
    ),
    path(
        "seg_vial/",
        views.SVView.as_view(),
        name="seg_vial",
    ),
    path(
        "dpt/",
        views.DPTView.as_view(),
        name="dpt",
    ),
    path(
        "consulta_ordenes_insp",
        views.HabsView.as_view(),
        name="consulta_ordenes_insp",
    ),
    path(
        "consulta_documentacion",
        views.DocumentView.as_view(),
        name="consulta_documentacion",
    ),
    path("empty", views.empty_view, name="empty"),
    path("get-template/", views.get_template_name, name="get_template"),
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
        "habilitaciones_form/",
        views.RenderHabilitacionForm.as_view(),
        name="habilitaciones_form",
    ),
    path(
        "verificaciones_form/",
        views.RenderVerificacionForm.as_view(),
        name="verificaciones_form",
    ),
    path(
        "certs_assignados/",
        views.ListCertificadosAssignView.as_view(),
        name="certs_asignados",
    ),
    path("certificados/", views.ListCertificadosView.as_view(), name="certificados"),
    path("vehiculos/", views.ListVehiculosView.as_view(), name="vehiculos"),
    path("cargaobleas/", views.carga_obleas, name="carga_obleas"),
    path("cargaobleas_check/", views.carga_obleas_check, name="carga_obleas_check"),
    path("cert_bound_confirm/", views.cert_bound_confirm, name="cert_bound_confirm"),
    path("resumenobleas/", views.resumen_obleas, name="resumen_obleas"),
    path(
        "cargahabilitacion/",
        views.carga_habilitacion,
        name="carga_habilitacion",
    ),
    path(
        "cargahabilitacion/<int:idhabilitacion>/<str:dominio>",
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
        name="consulta_habilitaciones_finales",
    ),
    path(
        "consulta_resumen_mensual/",
        views.consulta_resumen_mensual,
        name="consulta_resumen_mensual",
    ),
    path(
        "imprimir_resumen_mensual/<str:uuid>",
        views.PDFResumenMensual.as_view(),
        name="imprimir_resumen_mensual",
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

# URLS CCCF
cccf_urls = [
    path("cccf", CCCFView.as_view(), name="cccf"),
    path("cccf_list/", ListCCCFView.as_view(), name="cccf_list"),
    path(
        "cccf_carga/<int:nrocertificado>/<str:dominio>", carga_cccf, name="cccf_carga"
    ),
    path("cccf_carga/", carga_cccf, name="cccf_carga"),
    path(
        "cccf_anular/<int:nrocertificado>/<str:dominio>",
        AnularCCCF.as_view(),
        name="cccf_anular",
    ),
    path("cccf_form/", CCCFRenderForm.as_view(), name="cccf_form"),
    path("cccf_estado_error/", cccf_estado_error, name="cccf_estado_error"),
    path("cccf_estado_success/", cccf_estado_success, name="cccf_estado_success"),
    path("cccf_add_exceso/", add_cccf_exceso, name="cccf_add_exceso"),
    path("cccf_carga_precinto/", CargaPrecinto.as_view(), name="cccf_carga_precinto"),
    path("cccf_imprimir/<int:nrocertificado>", PDFCccf.as_view(), name="cccf_imprimir"),
    path(
        "cccf_exceso_table/",
        consulta_excesos,
        name="cccf_exceso_table",
    ),
    path(
        "cccf_modal_excesos/",
        get_cccf_modal_excesos,
        name="cccf_modal_excesos",
    ),
    path(
        "cccf_modal/<int:nrocertificado>/<str:dominio>",
        get_cccf_modal,
        name="cccf_modal",
    ),
    path(
        "ver_cccf/<int:nrocertificado>/<str:dominio>",
        VerCCCF.as_view(),
        name="ver_cccf",
    ),
    path("cccf_talleres", CccfTalleresList.as_view(), name="cccf_talleres"),
    path(
        "editar_taller_cccf/<int:idtaller>",
        editar_cccf_taller,
        name="editar_taller_cccf",
    ),
    path(
        "editar_taller_cccf_confirm",
        editar_cccf_taller,
        name="editar_taller_cccf_confirm",
    ),
    path(
        "usuarios_taller_cccf/<int:idtaller>",
        ver_cccf_usuarios,
        name="usuarios_taller_cccf",
    ),
    path("taller_edit_success", taller_edit_success, name="taller_edit_success"),
    path("taller_edit_failure", taller_edit_failure, name="taller_edit_failure"),
    path(
        "dar_de_baja_taller_cccf/<int:idtaller>",
        dar_de_baja_taller_cccf,
        name="dar_de_baja_taller_cccf",
    ),
    path(
        "taller_baja_confirm",
        dar_de_baja_taller_cccf_confirm,
        name="taller_baja_confirm",
    ),
]

# URLS RIO NEGRO
urlpatterns += [
    path("", include("rto_consultas_rn.urls")),
]

urlpatterns += cccf_urls

error_urls = [
    path(
        "cert_bound_error",
        views.cert_bound_error,
        name="cert_bound_error",
    ),
]

urlpatterns += error_urls

if settings.DEBUG:
    urlpatterns += [
        path("static/", serve, {"document_root": settings.STATIC_ROOT}),
    ]
    # For serving media files during development
    urlpatterns += staticfiles_urlpatterns()
