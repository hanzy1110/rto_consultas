import os
from django import forms
from .helpers import LOG_FILE, AuxData, map_fields
from .models import Estados, Tipovehiculo, Tipousovehiculo, Talleres
from .logging import configure_logger

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, HTML

logger = configure_logger(LOG_FILE)


def get_choices():
    aux_data = AuxData(
        query_fields=[],
        form_fields={
            "idestado": ("descripcion", Estados),
            "idtipouso": ("descripcion", Tipousovehiculo),
            "idtipovehiculo": ("descripcion", Tipovehiculo),
            "idtaller": ("nombre", Talleres),
        },
        parsed_names={"name": "name"},
    )
    logger.debug(aux_data)
    vals = map_fields(aux_data, Talleres)
    logger.debug(vals)

    choices = list(tuple(vals["idtaller"].items()))
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


class InspectionOrderForm(forms.Form):
    # Define form fields
    dominio = forms.CharField(
        label="Dominio",
        widget=forms.TextInput(attrs={"class": "txt", "style": "width: 150px"}),
    )
    ckPatenteMer = forms.BooleanField(
        label="P. Mercosur",
        required=False,
        widget=forms.CheckboxInput(
            attrs={"id": "ckPatenteMer", "name": "ckPatenteMer", "value": "1"}
        ),
    )
    modelo = forms.CharField(
        label="Año de Fabricación",
        widget=forms.TextInput(attrs={"class": "txt", "style": "width: 242px"}),
    )
    cccf = forms.CharField(
        label="CCCF Nro",
        widget=forms.TextInput(attrs={"class": "txt", "style": "width: 242px"}),
    )
    titular = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(attrs={"class": "txt", "style": "width: 242px"}),
    )
    servicios = forms.MultipleChoiceField(
        label="Seleccione uno o más servicios (máximo 4):",
        choices=[
            (
                1,
                "Servicio Turismo (Corredor de los Lagos Andino-Patagonico ley nº26654)",
            ),
            (2, "Servicio Escolares Intermunicipales/Contratado Ocasional"),
            (5, "Servicio Contratado"),
            (6, "Servicio Público"),
            (7, "Servicio Escolares Intermunicipales"),
            (8, "Servicio Contratado Ocasional"),
            (9, "Servicio Propio"),
            (11, "Servicio Turismo"),
        ],
        widget=forms.CheckboxSelectMultiple(),
    )

    def __init__(self, *args, **kwargs):
        super(InspectionOrderForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "col_w900 col_w900_last"
        self.helper.layout = Layout(
            Div(
                Field("dominio"),
                Field("ckPatenteMer"),
                css_class="tr",
            ),
            Div(
                Field("modelo"),
                css_class="tr",
            ),
            Div(
                Field("cccf"),
                css_class="tr",
            ),
            HTML("<tr><td>&nbsp;</td></tr>"),
            Div(
                Field("titular"),
                css_class="tr",
            ),
            HTML("<tr><td>&nbsp;</td></tr>"),
            Div(
                HTML("<b>Tipo de servicio</b>"),
                css_class="tr",
            ),
            Div(
                Field("servicios"),
                css_class="tr",
            ),
        )
