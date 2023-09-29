from django import forms
from .helpers import AuxData, map_fields
from .models import Estados, Tipovehiculo, Tipousovehiculo, Talleres


def get_choices(data: AuxData, model):
    return map_fields(data, model)


class ObleasPorTaller(forms.Form):
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
    fecha_desde = forms.DateField(max_length=100, required=True, label="Parameter 1")
    fecha_hasta = forms.DateField(required=True, label="Parameter 2")
    taller_id = forms.ChoiceField(
        # choices=[("option1", "Option 1"), ("option2", "Option 2")],
        choices=list(tuple(map_fields(aux_data, Talleres)["idtaller"])),
        required=True,
        label="Planta",
    )
