import os
from rto_consultas.helpers import TipoUsoAutocomplete, TallerAutocomplete_RN, LocalidadesAutocomplete_RN
from .models import Excepcion, Localidades, Talleres, Tipousovehiculo, Vehiculos
from rto_consultas.logging import configure_logger
from rto_consultas.name_schemas import DICTAMEN_CHOICES

from autocomplete import widgets as widgets_autocomplete
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
        choices=get_choices(),
        required=False,
        label="Planta",
    )


class ExcepcionesFirstForm(forms.ModelForm):
    fecha = forms.DateField(
        label="Fecha Creacion",
        widget=forms.DateInput(attrs={"class": "date", "type": "date"}),
    )
    fechahoradictamen = forms.DateField(
        label="Fecha Dictamen",
        widget=forms.DateInput(attrs={"class": "date", "type": "date"}),
    )

    idtipouso = forms.ModelChoiceField(
        label="Tipo Uso",
        queryset=Tipousovehiculo.objects.all(),
        widget=widgets_autocomplete.Autocomplete(
            # name="idtipouso",
            use_ac=TipoUsoAutocomplete
            # options=dict(model=Tipousovehiculo, item_label="descripcion", item_value="idtipouso")
        ),
    )

    idtaller = forms.ModelChoiceField(
        label="Planta",
        queryset=Talleres.objects.all(),
        widget=widgets_autocomplete.Autocomplete(
            # name="idtipouso",
            use_ac=TallerAutocomplete_RN,
            # options=dict(model=Tipousovehiculo, item_label="descripcion", item_value="idtipouso")
        ),
    )

    idlocalidadtitular = forms.ModelChoiceField(
        label="Localidad Titular",
        queryset=Localidades.objects.all(),
        widget=widgets_autocomplete.Autocomplete(
            # name="idtipouso",
            use_ac=LocalidadesAutocomplete_RN,
            # options=dict(model=Tipousovehiculo, item_label="descripcion", item_value="idtipouso")
        ),
    )
    idlocalidadconductor = forms.ModelChoiceField(
        label="Localidad Conductor",
        queryset=Localidades.objects.all(),
        widget=widgets_autocomplete.Autocomplete(
            # name="idtipouso",
            use_ac=LocalidadesAutocomplete_RN,
            # options=dict(model=Tipousovehiculo, item_label="descripcion", item_value="idtipouso")
        ),
    )
    resultado = forms.ChoiceField(
        choices=[(0,"Seleccione..."), (1,"Aprobado"), (2, "Desaprobado")],
        required=True,
        label="Resultado",
    )

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

    def __init__(self,editable=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        for f in self.fields.keys():
            self.fields[f].editable=editable

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
            "nrodoctitular",
            "nombretitular",
            "telefonotitular",
        ]
        conductor_fields = [
            "apellidoconductor",
            "nombreconductor",
            "nrodocconductor",
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
            "idtipouso",
            "companiaseguro",
            "nropoliza",
            "vanio",
            "modelovehiculo",
            "motornumero",
            "tipocombustible",
            "chasisnro",
            "nroejes",
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
                Div(Field("observaciondictamen", wrapper_class="form-group col-10"), css_class="mx-2 col-12"),
                HTML("<b>Planta Autorizada</b>"),
                Div(Field('idtaller', wrapper_class="form-group col-10"), css_class="mx-2 col-12"),
                css_class="card card-plain mt-2 box",
            ),

            Div(HTML("<b>Resultado</b>"),
                Field('resultado', wrapper_class="form-group col-10") ,css_class="card card-plain mt-2 box"),

        )
