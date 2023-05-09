from django.db.models import Q
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
# import django_tables2 as tables
from django_tables2 import SingleTableView
from django_tables2.config import RequestConfig
import re

from .models import Verificaciones, Certificadosasignadosportaller, Vehiculos, Certificados
from .models import Estados, Tipousovehiculo, Talleres
from .tables import VerificacionesTables, VehiculosTable, CertificadosTable, CertificadosAssignTable
from .helpers import handle_context, handle_query, AuxData

    
class ListVerificacionesView(SingleTableView, LoginRequiredMixin):
    # authentication_classes = [authentication.TokenAuthentication]
    model = Verificaciones
    paginate_by = 10
    template_name = "includes/list_table.html"
    context_object_name = "Verificaciones"
    table_class = VerificacionesTables

    aux_data = AuxData(query_fields=["dominiovehiculo",],
                        form_fields={"idestado": ("descripcion", Estados),
                                    "idtipouso":("descripcion", Tipousovehiculo) },
                        parsed_names={"dominiovehiculo": "Dominio Vehiculo",
                                        "idestado":"Estado Certificado",
                                        "idtipouso":"Tipo Uso Vehiculo"} 
                        )


    def get_queryset(self):
        page = self.request.GET.copy().pop("page", None)
        queryset = handle_query(self.request, self.model)

        if page:
            #Handle pagination...
            self.table_data = queryset
            table = self.get_table()
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = handle_context(context, self)
        return context

    
class ListCertificadosAssignView(SingleTableView, LoginRequiredMixin):
    # authentication_classes = [authentication.TokenAuthentication]
    model = Certificadosasignadosportaller
    paginate_by = 10
    template_name = "includes/list_table.html"
    context_object_name = "Certificados Asignados por taller"
    table_class = CertificadosAssignTable

    aux_data = AuxData(query_fields=["nrocertificado",],
                        form_fields={"idtaller":("nombre", Talleres)},
                        parsed_names={"nrocertificado": "Nro. Certificado",
                                        "disponible":"Disponible",
                                        "replicado":"Replicado"} 
                        )

    def get_queryset(self):
        page = self.request.GET.copy().pop("page", None)
        queryset = handle_query(self.request, self.model)

        if page:
            #Handle pagination...
            self.table_data = queryset
            table = self.get_table()
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = handle_context(context, self)
        return context


class ListVehiculosView(SingleTableView, LoginRequiredMixin):
    # authentication_classes = [authentication.TokenAuthentication]
    model = Vehiculos
    template_name = "includes/list_table.html"
    paginate_by = 10
    context_object_name = "Vehiculos"
    table_class = VehiculosTable

    aux_data = AuxData(query_fields=["dominio", "marca"],
                        form_fields={"idtipouso":("descripcion", Tipousovehiculo) },
                        parsed_names={"dominio": "Dominio Vehiculo",
                                    "marca":"Marca Vehiculo",
                                    "idtipouso":"Tipo Uso Vehiculo"} 
                        )

    def get_queryset(self):
        page = self.request.GET.copy().pop("page", None)
        queryset = handle_query(self.request, self.model)

        if page:
            #Handle pagination...
            self.table_data = queryset
            table = self.get_table()
            
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = handle_context(context, self)
        return context

    
class ListCertificadosView(SingleTableView, LoginRequiredMixin):
    # authentication_classes = [authentication.TokenAuthentication]
    model = Certificados
    template_name = "includes/list_table.html"
    paginate_by = 10
    context_object_name = "Certificados"
    table_class = CertificadosTable

    aux_data = AuxData(query_fields=["nrocertificado", "fecha", "anulado"],
                        form_fields={"idtaller":("nombre", Talleres)},
                        parsed_names={"nrocertificado": "Nro. Certificado",
                                    "anulado":"Anulado",
                                    "fecha":"Fecha",
                                    "idtaller":"Nombre Taller"} 
                        )

    def get_queryset(self):
        page = self.request.GET.copy().pop("page", None)
        queryset = handle_query(self.request, self.model)

        if page:
            #Handle pagination...
            self.table_data = queryset
            table = self.get_table()
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = handle_context(context, self)
        return context
