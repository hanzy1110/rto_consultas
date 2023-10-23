import os
from django import forms
from django.db.models import Model
from django.forms import widgets
from .helpers import AuxData, map_fields
from .models import Estados, Tipovehiculo, Tipousovehiculo, Talleres
from .logging import configure_logger

from dataclasses import asdict

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Div, Field, HTML, ButtonHolder, Submit

LOG_FILE = os.environ["LOG_FILE"]
logger = configure_logger(LOG_FILE)


DOCS = [(i, d) for i, d in enumerate(["", "DNI", "LC", "LE", "PAS", "CUIT"])]


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


# <input type="text" css_class="form-control" placeholder="Type here..." onfocus="focused(this)" onfocusout="defocused(this)">


class CustomRTOForm(forms.Form):
    def __init__(self, form_data: AuxData, model: Model, *args, **kwargs):
        super(CustomRTOForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout()

        for _, qf in enumerate(form_data.query_fields):
            input_type = form_data.types.get(qf, None)
            label = form_data.parsed_names.get(qf, None)
            attributes = form_data.attributes.get(qf, None)

            if input_type == "text":
                field = forms.CharField(
                    label=label,
                    widget=forms.TextInput(attrs=attributes),
                )
            elif input_type == "date":
                field = forms.DateField(
                    label=label,
                    widget=forms.DateInput(attrs={"class": "date", "type": "date"}),
                )
            elif input_type == "select":
                # TODO add more types of select!
                field = forms.ChoiceField(
                    choices=DOCS,
                    widget=forms.Select(),
                    initial="",  # Set the initial value if needed
                )
            else:
                field = None  # Handle other input types as needed

            if field:
                field.required = False
                self.fields[qf] = field

        # self.helper.layout.append(query_div)
        # self.helper.layout.append(field)

        descriptions = map_fields(form_data, model)
        logger.debug(f"DESCRIPTIONS => {descriptions}")

        for ff in form_data.form_fields:
            label = form_data.parsed_names.get(ff, None)
            attributes = form_data.attributes.get(ff, None)
            ids = form_data.ids.get(ff, None)
            desc = descriptions.get(ff, None)
            # TODO aca van las descripciopnes...
            cs = [(str(i), c) for i, c in enumerate(desc.values())]

            choices = [("", "")]
            choices.extend(cs)

            field = forms.ChoiceField(
                label=label,
                choices=choices,
                widget=forms.Select(),
                initial="",  # Set the initial value if needed
            )
            if field:
                field.required = False
                self.fields[ff] = field
            # self.helper.layout.append(Field(ff))
            # self.helper.layout.append(field)

        query_div = Div(
            *[Field(qf, css_class="form-control") for qf in form_data.query_fields],
            css_class="col-md-6",
        )
        form_div = Div(
            *[Field(ff, css_class="form-control") for ff in form_data.form_fields],
            css_class="col-md-6",
        )
        side_by_side = Row(
            Div(query_div, css_class="col"),
            Div(form_div, css_class="col"),
        )
        self.helper.layout = Layout(side_by_side)


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
