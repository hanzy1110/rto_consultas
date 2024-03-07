import os
from rto_consultas.helpers import (
    TipoUsoAutocomplete,
    TallerAutocomplete_RN,
    LocalidadesAutocomplete_RN,
)
from .models import Excepcion, Localidades, Talleres, Tipousovehiculo, Vehiculos
from rto_consultas.logging import configure_logger
from rto_consultas.name_schemas import DICTAMEN_CHOICES, TIPO_USO_CHOICES

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

    idlocalidadvehiculo = forms.ModelChoiceField(
        label="Localidad Vehiculo",
        queryset=Localidades.objects.all(),
        widget=widgets_autocomplete.Autocomplete(
            # name="idtipouso",
            use_ac=LocalidadesAutocomplete_RN,
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
        choices=[(0, "Seleccione..."), (1, "Aprobado"), (2, "Desaprobado")],
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
            "estado",
        ]

    def __init__(self, disable_edition=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        logger.info(f"disable_edition ==> {disable_edition}")
        disallowed_keys = list(
            filter(
                lambda x: x not in {"resultado", "observaciondictamen"},
                set(self.fields.keys()),
            )
        )
        for f in disallowed_keys:
            self.fields[f].disabled = disable_edition

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
                    css_class="form-group row box",
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
                    css_class="form-group row box",
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
                    css_class="form-group row box",
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
                    css_class="form-group row box",
                ),
                css_class="card card-plain mt-2 box",
            ),
            Div(
                HTML("<b>Observaciones Dictamen</b>"),
                HTML("<b>Fundamentación Dictamen</b>"),
                Div(
                    Field("observaciondictamen", wrapper_class="form-group col-10"),
                    css_class="mx-2 col-12",
                ),
                HTML("<b>Planta Autorizada</b>"),
                Div(
                    Field("idtaller", wrapper_class="form-group col-10"),
                    css_class="mx-2 col-12",
                ),
                css_class="card card-plain mt-2 box",
            ),
            Div(
                HTML("<b>Resultado</b>"),
                Field("resultado", wrapper_class="form-group col-10"),
                css_class="card card-plain mt-2 box",
            ),
        )

class ResumenMensualForm(forms.Form):
    fecha_desde = forms.DateField(
        required=True,
        label="Fecha Desde",
        widget=forms.DateInput(attrs={"class": "date", "type": "date"}),
    )
    fecha_hasta = forms.DateField(
        required=True,
        label="Fecha Hasta",
        widget=forms.DateInput(attrs={"class": "date", "type": "date"}),
    )
    id_taller = forms.ChoiceField(
        # choices=[("option1", "Option 1"), ("option2", "Option 2")],
        choices=get_choices(),
        required=True,
        label="Planta",
    )
    tipo_uso = forms.ChoiceField(
        # choices=[("option1", "Option 1"), ("option2", "Option 2")],
        choices=TIPO_USO_CHOICES,
        required=False,
        label="Tipo de Uso",
    )

    def __init__(self, *args, **kwargs):
        super(ResumenMensualForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "form-horizontal"

        self.helper.layout = Layout(
            Div(
                Field("fecha_desde", wrapper_class="form-group col-6"),
                Field("fecha_hasta", wrapper_class="form-group col-6"),
                Field("id_taller", wrapper_class="form-group col-6"),
                Field("tipo_uso", wrapper_class="form-group col-6"),
            )
        )


class ResumenMensualSV(ResumenMensualForm):
    tipo_uso = forms.ChoiceField(
        # choices=[("option1", "Option 1"), ("option2", "Option 2")],
        choices=[("vup", "Uso Particular")],
        required=False,
        label="Tipo de Uso",
    )


class ResumenMensualDPT(ResumenMensualForm):
    tipo_uso = forms.ChoiceField(
        # choices=[("option1", "Option 1"), ("option2", "Option 2")],
        choices=[("dpt", "Transp. Carga y Pasajeros")],
        required=True,
        label="Tipo de Uso",
    )


def route_form(tipo_uso, referer):
    if tipo_uso:
        match tipo_uso:
            case "vup":
                return ResumenMensualSV
            case "dpt":
                return ResumenMensualDPT
            case _:
                return ResumenMensualForm

    referer = referer[:-1].split("/")[-1]
    logger.debug(f"PARSED REFERER {referer}")
    match referer:
        case "seg_vial":
            return ResumenMensualSV
        case "seg_vial_auditoria":
            return ResumenMensualSV
        case "dpt":
            return ResumenMensualDPT
        case _:
            return ResumenMensualForm
