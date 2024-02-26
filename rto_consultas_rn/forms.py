import os
from rto_consultas.helpers import AuxData, map_fields
from .models import Excepcion, Talleres, Vehiculos
from rto_consultas.logging import configure_logger
from rto_consultas.name_schemas import DICTAMEN_CHOICES

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Div, Field, HTML, ButtonHolder, Submit

LOG_FILE = os.environ["LOG_FILE"]
logger = configure_logger(LOG_FILE)


def get_choices():
    vals = Talleres.objects.filter(activo__iexact=1).values_list("idtaller", "nombre")

    choices = list(vals)
    a = [("", "")]
    a.extend(choices)
    return a


class ObleasPorTaller(forms.Form):
    fecha_desde = forms.DateField(required=False, label="Fecha Desde")
    fecha_hasta = forms.DateField(required=False, label="Fecha Hasta")
    taller_id = forms.ChoiceField(
        # choices=[("option1", "Option 1"), ("option2", "Option 2")],
        choices=get_choices(),
        required=False,
        label="Planta",
    )


class ExcepcionesFirstForm(forms.ModelForm):
    # # TITULAR FIELDS:
    # tipopersona = forms.CharField(label="Tipo Persona")
    # apellidotitular = forms.CharField(label="Apellido Titular")
    # nombretitular = forms.CharField(label="Nombre Titular")
    # idlocalidadtitular = forms.CharField(label="Localidad Titular")
    # domiciliotitular = forms.CharField(label="Domicilio Titular")
    # emailtitular = forms.CharField(label="Email Titular")
    # nrodoctitual = forms.CharField(label="Nro Doc Titular")
    # nombretitular = forms.CharField(label="Apellido Titular")
    # telefonotitular = forms.CharField(label="Telefono Titular")

    # #EXCEPCION FIELDS:
    fecha = forms.DateField(
        label="Fecha Creacion",
        widget=forms.DateInput(attrs={"class": "date", "type": "date"}),
    )
    # estado = forms.ChoiceField(label="Dictamen", choices=DICTAMEN_CHOICES)
    fechahoradictamen = forms.DateField(
        label="Fecha Dictamen",
        widget=forms.DateInput(attrs={"class": "date", "type": "date"}),
    )
    # usuario = forms.CharField(label="Usuario Creacion")
    # usuariodictamen = forms.CharField(label="Usuario Dictamen")

    class Meta:
        model = Excepcion
        # fields = "__all__"
        exclude = [
            "idexcepcion",
            "modificado",
            "viedmapatagones",
            "codigotitular",
            "notifyactive",
            "idcategoria",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        excepcion_fields = [
            "fecha",
            "estado",
            "fechahoradictamen",
            "usuario",
            "usuariodictamen",
        ]

        titular_fields = [
            "tipopersona",
            "apellidotitular",
            "nombretitular",
            "idlocalidadtitular",
            "domiciliotitular",
            "emailtitular",
            "nrodoctitual",
            "nombretitular",
            "telefonotitular",
        ]
        conductor_fields = [
            "apellidoconductor",
            "nombreconductor",
            "domicilioconductor",
            "idlocalidadconductor",
        ]

        vehicle_fields = [
            "dominio",
            "marcavehiculo",
            "idlocalidadvehiculo",
            "motormarca",
            "motoranio",
            "chasismarca",
            "chasisanio",
            "idtipovehiculo",
            "companiaseguro",
            "nropoliza",
            "vanio",
            "modelovehiculo",
            "motornumero",
            "tipocombustible",
            "chasisnro",
            "nroejes",
            "idtipouso",
            "ultimorecpatente",
        ]

        self.helper.layout = Layout(
            Div(
                HTML("<b>Datos de la Excepción</b>"),
                Div(
                    *[
                        Field(k, wrapper_class="form-group col-4")
                        for k in excepcion_fields
                    ],
                    css_class="form-group row box"
                ),
                css_class="card card-plain mt-2 box",
            ),
            Div(
                HTML("<b>Datos del Vehiculo</b>"),
                Div(
                    *[
                        Field(k, wrapper_class="form-group col-4")
                        for k in vehicle_fields
                    ],
                    css_class="form-group row box"
                ),
                css_class="card card-plain mt-2 box",
            ),
            Div(
                HTML("<b>Datos del Titular</b>"),
                Div(
                    *[
                        Field(k, wrapper_class="form-group col-4")
                        for k in titular_fields
                    ],
                    css_class="form-group row box"
                ),
                css_class="card card-plain mt-2 box",
            ),
            Div(
                HTML("<b>Datos del Conductor</b>"),
                Div(
                    *[
                        Field(k, wrapper_class="form-group col-4")
                        for k in conductor_fields
                    ],
                    css_class="form-group row box"
                ),
                css_class="card card-plain mt-2 box",
            ),
            Div(
                HTML("<b>Observaciones Dictamen</b>"),
                HTML("<b>Fundamentación Dictamen</b>"),
                Div(Field("observaciondictamen", wrapper_class="form-group col-12")),
                HTML("<b>Resultado</b>"),
                css_class="card card-plain mt-2 box",
            ),
        )


class ExcepcionesSecondForm(forms.ModelForm):
    class Meta:
        model = Excepcion
        fields = "__all__"


class ExcepcionesVehiculosForm(forms.ModelForm):
    class Meta:
        model = Vehiculos
        fields = "__all__"
