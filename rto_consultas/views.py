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


def handle_args(query_params, queryset):
    numeric_test = re.compile(r"^\d+$")
    cleaned_query = {k:v for k,v in query_params.items() if v}
    for key, arg in cleaned_query.items():
        if numeric_test.match(str(arg)):
            query = Q(**{f"{key}__exact":int(arg)})
        elif "dominio" in key: 
            query = Q(**{f"{key}__exact":arg}) 
        elif isinstance(arg, str):
            query = Q(**{f"{key}__icontains":arg})
        else:
            return queryset

        queryset = queryset.filter(query)

    return queryset

def handle_query(request, model):
    query = request.GET.copy()
    sort = query.pop("sort", None)
    page = query.pop("page", None)
    queryset = model.objects.all()
    if query:
        queryset = handle_args(query, queryset)
    if sort:
        queryset = queryset.order_by(sort[0])
    return queryset

def handle_form(form_fields, model):
    values = {}
    for field in form_fields.keys():
        val = model.objects.values_list(field, flat=True).distinct() 
        values[field] = val
    return values

def map_fields(form_fields, description_fields, model):
    values = {}
    if not description_fields:
        return {k:{0:"Falso", 1:"Verdadero"} for k in form_fields}

    for field, (dfield, dmodel) in zip(form_fields.keys(), description_fields):
        val = model.objects.values_list(field, flat=True).distinct() 
        descriptions = dmodel.objects.values_list(dfield, flat=True).distinct() 
        values[field] = {v:d for v,d in zip(val, descriptions)}

    return values


def handle_context(context, view):
    val_dict = handle_form(view.form_fields, view.model) 
    context["form_fields"] = {k:{name:vals} for (k, name), vals in zip(view.form_fields.items(),
                                                                         val_dict.values())}
    context["descriptions"] = map_fields(view.form_fields, 
                                        view.description_fields, 
                                        view.model)

    # context["parsed_fields"] = view.parsed_fields
    fields = view.model._meta.fields
    context["fields"] = fields
    # context["query_fields"] = list(filter(lambda x: x.name in view.query_fields and x.name not in view.form_fields, fields))
    context["query_fields"] = view.query_fields 
    return context
    
class ListVerificacionesView(SingleTableView, LoginRequiredMixin):
    # authentication_classes = [authentication.TokenAuthentication]
    model = Verificaciones
    paginate_by = 10
    template_name = "includes/list_table.html"
    context_object_name = "Verificaciones"
    table_class = VerificacionesTables

    # query_fields = {
    #     "dominiovehiculo",
    #     "idestado",
    #     "idtipouso"
    # }

    query_fields = {
        "dominiovehiculo":"Dominio",
    }

    form_fields = {
        "idestado": "Estado Certificado",
        "idtipouso":"Tipo de Uso"
    }
    description_fields = {
        ("descripcion", Estados),
        ("descripcion", Tipousovehiculo)
    }

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
    # query_fields = {
    #     "nrocertificado",
    #     "disponible",
    #     "replicado"
    # }
    query_fields = {
        "nrocertificado":"Nro. Certificado",
    }
    form_fields = {
        "disponible",
        "replicado"
    }
    description_fields = {}

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
    # query_fields = {
    #     "dominio",
    #     "idtipouso",
    #     "marca"
    # }
    query_fields = {
        "dominio":"Dominio",
        "marca":"Marca"
    }
    form_fields = {
        "idtipouso":"Tipo de Uso",
    }

    description_fields = {
        ("descripcion", Tipousovehiculo)
    }

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
    # query_fields = {
    #     "nrocertificado",
    #     "idtaller",
    #     "fecha",
    #     "anulado"
    #     }
    query_fields = {
        "nrocertificado":"Nro. Certificado",
        "fecha":"Fecha",
        "anulado":"Anulado"
        }
    form_fields = {
        "idtaller":"Taller",
        }

    description_fields = {
        ("nombre", Talleres)
    }

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
