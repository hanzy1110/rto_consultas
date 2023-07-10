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
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path("accounts/", include("django.contrib.auth.urls")),
    path('verificaciones/', views.ListVerificacionesView.as_view(),
         name="verificaciones"),
    path('certs_assignados/', views.ListCertificadosAssignView.as_view(),
         name="certs_asignados"),
    path('certificados/', views.ListCertificadosView.as_view(),
         name="certificados"),
    path('vehiculos/', views.ListVehiculosView.as_view(),
         name="vehiculos"),
    # path('vw_verificaciones/', views.ListVWVerificacionesView.as_view(),
    #      name="vw_verificaciones"),
    # path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('', include('admin_soft.urls'), name=admin),
]
