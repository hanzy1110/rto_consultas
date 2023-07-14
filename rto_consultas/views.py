from django.db.models import Model
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_tables2 import SingleTableView, Table


from .models import (
    Localidades,
    Provincias,
    Verificaciones,
    Certificadosasignadosportaller,
    Vehiculos,
    Certificados,
    Categorias,
)
from .models import Estados, Tipousovehiculo, Talleres
from .tables import (
    VerificacionesTables,
    VehiculosTable,
    CertificadosTable,
    CertificadosAssignTable,
)
from .helpers import handle_context, handle_query, AuxData


class CustomRTOView(SingleTableView, LoginRequiredMixin):
    model: Model
    paginate_by: int
    template_name: str
    context_object_name: str
    table_class: Table
    aux_data: AuxData

    def get_queryset(self):
        page = self.request.GET.copy().pop("page", None)
        queryset = handle_query(self.request, self.model, self.aux_data.fecha_field)

        if page:
            # Handle pagination...
            self.table_data = queryset
            self.get_table()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = handle_context(context, self)
        return context


class ListVerificacionesView(CustomRTOView):
    # authentication_classes = [authentication.TokenAuthentication]
    model = Verificaciones
    paginate_by = 10
    template_name = "includes/list_table_verificaciones.html"
    context_object_name = "Verificaciones"
    table_class = VerificacionesTables

    aux_data = AuxData(
        query_fields=[
            "dominiovehiculo",
            "nrocertificado",
            "fecha_desde",
            "fecha_hasta",
        ],
        form_fields={
            "idestado": ("descripcion", Estados),
            "idtipouso": ("descripcion", Tipousovehiculo),
            # "idcategoria": ("descripcion", Categorias),
            "idtaller": ("nombre", Talleres),
        },
        parsed_names={
            "dominiovehiculo": "Dominio Vehiculo",
            "idestado": "Estado Certificado",
            "idtipouso": "Tipo Uso Vehiculo",
            "nrocertificado": "Nro. Certificado",
            "fecha_desde": "Fecha Desde",
            "fecha_hasta": "Fecha Hasta",
            # "categoria": "Categorias",
            "idtaller": "Nombre Taller",
        },
        ids={
            "dominiovehiculo": "#txtDominio",
            "fecha_desde": "#txtFechaD",
            "fecha_hasta": "#txtFechaH",
            "nrocertificado": "Nro. Certificado",
        },
        types={
            "dominiovehiculo": "text",
            "fecha_desde": "date",
            "fecha_hasta": "date",
            "nrocertificado": "text",
        },
    )



class ListCertificadosAssignView(CustomRTOView):
    # authentication_classes = [authentication.TokenAuthentication]
    model = Certificadosasignadosportaller
    paginate_by = 10
    template_name = "includes/list_table.html"
    context_object_name = "Certificados Asignados por taller"
    table_class = CertificadosAssignTable

    aux_data = AuxData(
        query_fields=[
            "nrocertificado",
            "fecha_desde",
            "fecha_hasta",
        ],
        form_fields={
            "idtaller": ("nombre", Talleres),
            "disponible": (None, None),
            "replicado": (None, None),
        },
        parsed_names={
            "nrocertificado": "Nro. Certificado",
            "disponible": "Disponible",
            "idtaller": "Nombre Taller",
            "replicado": "Replicado",
            "fecha_desde": "Fecha Desde",
            "fecha_hasta": "Fecha Hasta",
        },
        ids={
            "nrocertificado": "#txtNroCertificado",
            "fecha_desde": "#txtFechaD",
            "fecha_hasta": "#txtFechaH",
        },
        types={
            "fecha_desde": "date",
            "fecha_hasta": "date",
            "nrocertificado": "text",
        },
        fecha_field="fechacarga"
    )


class ListVehiculosView(CustomRTOView):
    # authentication_classes = [authentication.TokenAuthentication]
    model = Vehiculos
    template_name = "includes/list_table.html"
    paginate_by = 10
    context_object_name = "Vehiculos"
    table_class = VehiculosTable

    aux_data = AuxData(
        query_fields=["dominio", "marca"],
        form_fields={"idtipouso": ("descripcion", Tipousovehiculo)},
        parsed_names={
            "dominio": "Dominio Vehiculo",
            "marca": "Marca Vehiculo",
            "idtipouso": "Tipo Uso Vehiculo",
        },
        ids={"dominiovehiculo": "#txtDominio", "marca": "#txtMarca"},
        types={
            "marca": "text",
            "dominio": "text",
        },
    )


class ListCertificadosView(CustomRTOView):
    # authentication_classes = [authentication.TokenAuthentication]
    model = Certificados
    template_name = "includes/list_table.html"
    paginate_by = 10
    context_object_name = "Certificados"
    table_class = CertificadosTable

    aux_data = AuxData(
        query_fields=["nrocertificado", "fecha", "anulado"],
        form_fields={"idtaller": ("nombre", Talleres)},
        parsed_names={
            "nrocertificado": "Nro. Certificado",
            "anulado": "Anulado",
            "fecha": "Fecha",
            "idtaller": "Nombre Taller",
        },
        ids={
            "nrocertificado": "#txtNroCertificado",
            "fecha": "#txtFechaD",
        },
        types={
            "nrocertificado": "text",
            "fecha": "date",
            "anulado": "text",
        },
    )


class VerVerificacion(DetailView,LoginRequiredMixin):
    model: Verificaciones
    template_name = "includes/ver_verificaciones.html"
    context_object_name: str
    aux_data: AuxData

    def get_object(self):
        query_params = self.request.GET.copy()
        id_taller = self.kwargs["idtaller"]
        id_verificacion = self.kwargs["idverificacion"]
        verificacion = (Verificaciones.objects
                        .select_related("dominiovehiculo", "idestado", "codigotitular","idtaller")
                        .get(idverificacion=id_verificacion, idtaller=id_taller))

        print(verificacion)
        self.verificacion = verificacion
        return verificacion

    def get_total_values(self,):

        def sum_appropriatelly(values):
            return sum([float(v) for v in values if v])
        MToTara = sum_appropriatelly([self.verificacion.eje1_tara , self.verificacion.eje2_tara , self.verificacion.eje3_tara , self.verificacion.eje4_tara])
        MToFI = sum_appropriatelly([self.verificacion.eje1_fzaizq , self.verificacion.eje2_fzaizq , self.verificacion.eje3_fzaizq , self.verificacion.eje4_fzaizq])
        MToFD = sum_appropriatelly([self.verificacion.eje1_fzader , self.verificacion.eje2_fzader , self.verificacion.eje3_fzader , self.verificacion.eje4_fzader])
        MToEf = round((((MToFI + MToFD) / (MToTara * 9.81)) * 100), 2);
        return MToTara, MToFI, MToFD, MToEf

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cert = (
            Certificados.objects
                # .select_related("idcategoria")
                .filter(idverificacion_id__exact=self.kwargs["idverificacion"],
                        idtaller_id__exact=self.kwargs["idtaller"])
                .values()
                )
        categoria = (Categorias.objects
                               .get(idcategoria__exact=cert[0]["idcategoria"])
                               .descripcion)

        estado = (Estados.objects
                               .get(idestado__exact=cert[0]["idestado"])
                               .descripcion)

        localidad = (Localidades.objects
                               .get(idlocalidad__exact=self.verificacion.pidlocalidad)
                     )


        # provincia = (Provincias.objects
        #                        .get(idprovincia__exact=localidad.idprovincia)
        #                        .descripcion)

        context["nrocertificado"] = cert[0]["nrocertificado"]
        context["observaciones"] = cert[0]["observaciones"]
        context["vigenciahasta"] = cert[0]["vigenciahasta"]
        context["estado"] = estado
        context["categoria"] = categoria
        context["provincia"] = localidad.idprovincia.descripcion
        context["localidad"] = localidad.descripcion
        # TODO AGREGAR COMBO DOC
        context["comboDoc"] = []
        # TODO AGREGAR EL QUERY DE ADJUNTOS Y LAS URLS
        adjuntos = []
        context["certificado"] = cert[0]
        context["adjuntos"] = adjuntos
        context["mostrarJu"] = ""
        context["mostrarFi"] = ""
        MToTara, MToFI, MToFD, MToEf = self.get_total_values()
        context["mto_tara"] = MToTara
        context["mto_fi"] = MToFI
        context["mto_der"] = MToFD
        context["mto_eficiencia"] = MToEf

        # context = handle_context(context, self)
        return context
