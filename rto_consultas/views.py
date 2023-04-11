from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Verificaciones, Certificadosasignadosportaller, Vehiculos, Certificados


class ListVerificacionesView(ListView, LoginRequiredMixin):
    # authentication_classes = [authentication.TokenAuthentication]
    model = Verificaciones
    paginate_by = 10
    template_name = "includes/list_table.html"
    context_object_name = "Verificaciones"

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
        context["fields"] = self.model._meta.fields()
        context["query_fields"] = self.model._meta.fields()
        return context


class ListCertificadosAssignView(ListView, LoginRequiredMixin):
    # authentication_classes = [authentication.TokenAuthentication]
    model = Certificadosasignadosportaller
    paginate_by = 10
    template_name = "includes/list_table.html"
    context_object_name = "Certificados Asignados por taller"

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
        context["fields"] = self.model._meta.fields()
        context["query_fields"] = self.model._meta.fields()
        return context


class ListVehiculosView(ListView, LoginRequiredMixin):
    # authentication_classes = [authentication.TokenAuthentication]
    model = Vehiculos
    template_name = "includes/list_table.html"
    paginate_by = 10
    context_object_name = "Vehiculos"

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
        context["fields"] = self.model._meta.fields()
        context["query_fields"] = self.model._meta.fields()
        return context


class ListCertificadosView(ListView, LoginRequiredMixin):
    # authentication_classes = [authentication.TokenAuthentication]
    model = Certificados
    template_name = "includes/list_table.html"
    paginate_by = 10
    context_object_name = "Certificados"

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
        context["fields"] = self.model._meta.fields()
        context["query_fields"] = self.model._meta.fields()
        return context
