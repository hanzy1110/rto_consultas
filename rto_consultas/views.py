from django.db.models import Q
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
# import django_tables2 as tables
from django_tables2 import SingleTableView
import re

from .models import Verificaciones, Certificadosasignadosportaller, Vehiculos, Certificados
from .tables import VerificacionesTables, VehiculosTable, CertificadosTable, CertificadosAssignTable


def handle_args(query_params, queryset):
    numeric_test = re.compile(r"^\d+$")
    cleaned_query = {k:v for k,v in query_params.items() if v}
    for key, arg in cleaned_query.items():
        if numeric_test.match(str(arg)):
            query = Q(**{f"{key}__exact":int(arg)})
        # elif "dominio" in key: 
        #     query = Q(**{f"{key}__icontains":arg}) 
        elif isinstance(arg, str):
            query = Q(**{f"{key}__icontains":arg})
        else:
            return queryset
        return queryset.filter(query)

def handle_query(request, model):
    query = request.GET.copy()
    sort = query.pop("sort", None)
    queryset = model.objects.all()
    if query:
        queryset = handle_args(query, queryset)
    if sort:
        queryset = queryset.order_by(sort[0])
    return queryset

class ListVerificacionesView(SingleTableView, LoginRequiredMixin):
    # authentication_classes = [authentication.TokenAuthentication]
    model = Verificaciones
    paginate_by = 10
    template_name = "includes/list_table.html"
    context_object_name = "Verificaciones"
    table_class = VerificacionesTables
    query_fields = {
        "dominiovehiculo",
        "idestado",
        "idtipouso"
    }

    def get_queryset(self):
        return handle_query(self.request, self.model)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields = self.model._meta.fields
        context["fields"] = fields
        context["query_fields"] = list(filter(lambda x: x.name in self.query_fields, fields))
        return context


class ListCertificadosAssignView(SingleTableView, LoginRequiredMixin):
    # authentication_classes = [authentication.TokenAuthentication]
    model = Certificadosasignadosportaller
    paginate_by = 10
    template_name = "includes/list_table.html"
    context_object_name = "Certificados Asignados por taller"
    table_class = CertificadosAssignTable
    query_fields = {
        "nrocertificado",
        "disponible",
        "replicado"
    }

    def get_queryset(self):
        return handle_query(self.request, self.model)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields = self.model._meta.fields
        context["fields"] = fields
        context["query_fields"] = list(filter(lambda x: x.name in self.query_fields, fields))
        return context


class ListVehiculosView(SingleTableView, LoginRequiredMixin):
    # authentication_classes = [authentication.TokenAuthentication]
    model = Vehiculos
    template_name = "includes/list_table.html"
    paginate_by = 10
    context_object_name = "Vehiculos"
    table_class = VehiculosTable
    query_fields = {
        "dominio",
        "idtipouso",
        "marca"
    }

    def get_queryset(self):
        return handle_query(self.request, self.model)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields = self.model._meta.fields
        context["fields"] = fields
        context["query_fields"] = list(filter(lambda x: x.name in self.query_fields, fields))
        return context


class ListCertificadosView(SingleTableView, LoginRequiredMixin):
    # authentication_classes = [authentication.TokenAuthentication]
    model = Certificados
    template_name = "includes/list_table.html"
    paginate_by = 10
    context_object_name = "Certificados"
    table_class = CertificadosTable
    query_fields = {
        "nrocertificado",
        "idtaller",
        "fecha",
        "anulado"
        }

    def get_queryset(self):
        return handle_query(self.request, self.model)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields = self.model._meta.fields
        context["fields"] = fields
        context["query_fields"] = list(filter(lambda x: x.name in self.query_fields, fields))
        return context
