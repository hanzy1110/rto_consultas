import os
from rto_consultas.helpers import AuxData, map_fields, get_items_autocomplete
from .models import Excepcion, Talleres, Tipousovehiculo, Vehiculos
from rto_consultas.logging import configure_logger
from rto_consultas.name_schemas import DICTAMEN_CHOICES

from autocomplete import HTMXAutoComplete, widgets as widgets_autocomplete
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


class TipoUsoAutocomplete(HTMXAutoComplete):
    name = "idtipouso"
    # multiselect = True
    # minimum_search_length = 0
    _item_label = "descripcion"
    _item_value = "idtipouso"

    def get_items(self, *args, **kwargs):
        logger.info(f"PARAMS LABEL => {self._item_label},VALUE => {self._item_value}, {self.route_name}")
        return super().get_items(self, *args, **kwargs)

    class Meta:
        model = Tipousovehiculo
        # item_label = "descripcion"
        # item_value = "idtipouso"

class ExcepcionesFirstForm(forms.ModelForm):
    fecha = forms.DateField(
        label="Fecha Creacion",
        widget=forms.DateInput(attrs={"class": "date", "type": "date"}),
    )
    fechahoradictamen = forms.DateField(
        label="Fecha Dictamen",
        widget=forms.DateInput(attrs={"class": "date", "type": "date"}),
    )

    idtipouso = forms.ChoiceField(
        label="Tipo Uso",
        # queryset=Tipousovehiculo.objects.all(),
        widget=widgets_autocomplete.Autocomplete(
            name="idtipouso",
            use_ac= TipoUsoAutocomplete
            # options=dict(model=Tipousovehiculo, item_label="descripcion", item_value="idtipouso")
        ),
    )


    idtaller = forms.ChoiceField(
        choices=get_choices(),
        required=False,
        label="Planta",
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
                HTML("<b>Planta Autorizada</b>"),
                Div(Field('idtaller', wrapper_class="form-group col-12")),
                css_class="card card-plain mt-2 box",
            ),

            Div(HTML("<b>Resultado</b>"),css_class="card card-plain mt-2 box"),
        )


class ExcepcionesSecondForm(forms.ModelForm):
    class Meta:
        model = Excepcion
        fields = "__all__"


class ExcepcionesVehiculosForm(forms.ModelForm):
    class Meta:
        model = Vehiculos
        fields = "__all__"
