import os
from rto_consultas.helpers import AuxData, map_fields
from .models import Talleres
from rto_consultas.logging import configure_logger

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


class ObleasPorTaller_RN(forms.Form):
    fecha_desde = forms.DateField(required=False, label="Fecha Desde")
    fecha_hasta = forms.DateField(required=False, label="Fecha Hasta")
    taller_id = forms.ChoiceField(
        # choices=[("option1", "Option 1"), ("option2", "Option 2")],
        choices=get_choices(),
        required=False,
        label="Planta",
    )
