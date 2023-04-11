from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
# import django_tables2 as tables
from django_tables2 import SingleTableView

from .models import Verificaciones, Certificadosasignadosportaller, Vehiculos, Certificados


class ListVerificacionesView(SingleTableView, LoginRequiredMixin):
    # authentication_classes = [authentication.TokenAuthentication]
    model = Verificaciones
    paginate_by = 10
    template_name = "includes/list_table.html"
    context_object_name = "Verificaciones"
    query_fields = {
        "dominiovehiculo",
        "idestado",
        "idtipouso"
    }

    def get_queryset(self):
        # return self.model.objects.prefectch_related().all()[:5]
        query = self.request.GET
        if query:
            for field,value in query.items():
                return self.model.objects.filter(**{f"{field}__icontains":value})
        else:
            return self.model.objects.all()

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
    query_fields = {
        "nrocertificado",
        "disponible",
        "replicado"
    }

    def get_queryset(self):
        # return self.model.objects.prefectch_related().all()[:5]
        query = self.request.GET
        if query:
            for field,value in query.items():
                return self.model.objects.filter(**{f"{field}__icontains":value})
        else:
            return self.model.objects.all()

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
    query_fields = {
        "dominio",
        "idtipouso",
        "marca"
    }

    def get_queryset(self):
        # return self.model.objects.prefectch_related().all()[:5]
        query = self.request.GET
        if query:
            for field,value in query.items():
                return self.model.objects.filter(**{f"{field}__icontains":value})
        else:
            return self.model.objects.all()

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
    query_fields = {
        "nrocertificado",
        "idtaller",
        "fecha",
        "anulado"
        }

    def get_queryset(self):
        # return self.model.objects.prefectch_related().all()[:5]
        query = self.request.GET
        if query:
            for field,value in query.items():
                return self.model.objects.filter(**{f"{field}__icontains":value})
        else:
            return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields = self.model._meta.fields
        context["fields"] = fields
        context["query_fields"] = list(filter(lambda x: x.name in self.query_fields, fields))
        return context
