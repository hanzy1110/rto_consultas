import os
from typing import Union
from django import forms
from django.db.models import Model
from django.forms import widgets
from .helpers import AuxData, map_fields
from .models import CccfCertificados, Estados, Tipovehiculo, Tipousovehiculo, Talleres
from .logging import configure_logger

from dataclasses import asdict

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Div, Field, HTML, ButtonHolder, Submit

LOG_FILE = os.environ["LOG_FILE"]
logger = configure_logger(LOG_FILE)

from .name_schemas import *


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


class CustomRTOForm(forms.Form):
    def __init__(self, form_data: AuxData, model: Model, *args, **kwargs):
        super(CustomRTOForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout()

        for _, qf in enumerate(form_data.query_fields):
            input_type = form_data.types.get(qf, None)
            label = form_data.parsed_names.get(qf, None)
            attributes = form_data.attributes.get(qf, None)
            additional_field = None

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
                    label="Tipo Doc.",
                    choices=DOCS,
                    widget=forms.Select(),
                    initial="",  # Set the initial value if needed
                )
                additional_field = forms.CharField(
                    label="Nro. DNI",
                    widget=forms.TextInput(attrs=attributes),
                )
            else:
                field = None  # Handle other input types as needed

            if field:
                field.required = False
                self.fields[qf] = field
            if additional_field:
                additional_field.required = False
                self.fields["nro_dni"] = additional_field

        # self.helper.layout.append(query_div)
        # self.helper.layout.append(field)

        descriptions = map_fields(form_data, model)

        for ff in form_data.form_fields:
            if "estado" in ff:
                cs = [
                    (str(i + 1), c) for i, c in enumerate(ESTADO_CERTIFICADO.values())
                ]
            elif "uso" in ff:
                cs = [(str(i + 1), c) for i, c in enumerate(TIPO_USO_VEHICULO.values())]
            elif "taller" in ff:
                desc = descriptions.get(ff, None)
                cs = list(desc.items())
            else:
                desc = descriptions.get(ff, None)
                # TODO aca van las descripciopnes...
                cs = [(str(i), c) for i, c in enumerate(desc.values())]

            label = form_data.parsed_names.get(ff, None)
            attributes = form_data.attributes.get(ff, None)
            ids = form_data.ids.get(ff, None)

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

        # if "dominio" in form_data.query_fields:
        #     form_data.query_fields.pop(form_data.query_fields.index("dominio"))
        #     dom_div = Div(Field("dominio", css_class="form-control input-sm"))

        #     aux_div = Div(
        #         *[Field(qf, css_class="form-control input-sm") for qf in form_data.query_fields],
        #         css_class='field-group',
        #         style='display: none;'
        #     )
        #     query_div=Div(
        #         dom_div,
        #         aux_div
        #     )
        # else:

        #     query_div = Div(
        #         *[Field(qf, css_class="form-control input-sm") for qf in form_data.query_fields],
        #     )

        query_div = Div(
            *[
                Field(qf, css_class="form-control input-sm")
                for qf in form_data.query_fields
            ],
        )
        form_div = Div(
            *[
                Field(ff, css_class="form-control input-sm")
                for ff in form_data.form_fields
            ],
        )

        side_by_side = Row(
            Div(query_div),
            Div(form_div),
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


class ConsultaDPTForm(forms.Form):
    dominio = forms.CharField(
        label="Dominio",
        widget=forms.TextInput(attrs={"class": "txt", "style": "width: 150px"}),
    )

    consulta = forms.ChoiceField(
        # choices=[("option1", "Option 1"), ("option2", "Option 2")],
        choices=[("", ""), (1, "Dominio"), (2, "Habilitación")],
        required=False,
        label="Tipo de Consulta",
    )

    def __init__(self, *args, **kwargs):
        super(ConsultaDPTForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "col_w900 col_w900_last"
        self.helper.layout = Layout(
            Div(
                Field("dominio"),
                Field("dominio"),
                css_class="tr",
            ),
            Div(
                Field("consulta"),
                css_class="tr",
            ),
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
    usuariodictamen = forms.CharField(
        label="Emitido por",
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

    def __init__(self, initial: Union[None, dict[str, str]] = None, *args, **kwargs):
        super(InspectionOrderForm, self).__init__(*args, **kwargs)

        if initial:
            for k, v in initial.items():
                try:
                    self.fields[k].initial = v
                except Exception as e:
                    logger.warn(f"ERROR FOUND => {e}")
                    pass

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


class CCCFForm(forms.ModelForm):
    cuit = forms.CharField(label="CUIT")
    razon_social = forms.CharField(label="Razon Social")

    class Meta:
        model = CccfCertificados
        # fields = "__all__"
        fields = (
            # Primero
            "nrocertificado",
            "fechacalibracion",
            "fechavencimiento",
            # Segundo
            "cuit",
            "razon_social",
            "usuario",
            # Tercero
            "dominio",
            "nrointerno",
            "kilometraje",
            # Cuarto
            "tacmarca",
            "tactipo",
            "tacmodelo",
            "tacnroserie",
            "relw",
            "constantek",
            "rodado",
            "precinto",
            "impresora",
            "observaciones",
        )

    def __init__(self, *args, **kwargs):
        super(CCCFForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_id = "formCargaCert"
        # self.helper.form_method = "post"
        # self.helper.form_class = "form-horizontal"
        # self.helper.form_enctype = "multipart/form-data"

        self.helper.layout = Layout(
            Div(
                HTML("<h2>Datos del Certificado</h2>"),
                Field("nrocertificado"),
                Field("fechacalibracion"),
                Field("fechavencimiento"),
                css_class="card-body"
                # template="forms/cccf_layout.html",
            ),
            Div(
                HTML("<h2>Datos del Propietario</h2>"),
                Field("cuit"),
                Field("razonsocial"),
                Field("usuario"),
                css_class="card-body",
            ),
            Div(
                HTML("<h2>Datos del Vehiculo</h2>"),
                Field("dominio"),
                Field("nrointerno"),
                Field("kilometraje"),
                css_class="card-body",
            ),
            HTML("<h2>Datos del Tacografo</h2>"),
            Div(
                "tacmarca",
                "tactipo",
                "tacmodelo",
                "tacnroserie",
                "relw",
                "constantek",
                "rodado",
                "precinto",
                "impresora",
                "observaciones",
                css_class="card-body",
            ),
        )


class InformesForm(forms.Form):
    txtNroInforme = forms.CharField(
        label="Nro Informe",
        widget=forms.TextInput(
            attrs={"class": "form-control input-sm", "id": "txtNroInforme"}
        ),
        required=True,
    )

    txtCantHojas = forms.CharField(
        label="Cant. Hojas/Discos",
        widget=forms.TextInput(
            attrs={"class": "form-control input-sm", "id": "txtCantHojas"}
        ),
        required=True,
    )

    hfAdjuntos = forms.CharField(
        widget=forms.HiddenInput(attrs={"id": "hfAdjuntos"}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(InformesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Div(
                Div(
                    Field("txtNroInforme", wrapper_class="col-md-4"),
                    css_class="form-group",
                ),
                Div(
                    Field("txtCantHojas", wrapper_class="col-md-4"),
                    css_class="form-group",
                ),
                Div(
                    HTML(
                        '<label class="col-md-3 control-label">&nbsp;</label>'
                        '<div class="col-md-8">'
                        '   <span class="btn btn-success fileinput-button">'
                        '       <i class="glyphicon glyphicon-plus"></i>'
                        '       <span id="upload">Adjuntar Archivos...</span>'
                        "   </span><br/><br/>"
                        '   <span id="status"></span>'
                        '   <ul style="list-style: none;" id="files"></ul>'
                        '   <span id="resultado"></span>'
                        "   {% crispy form %}"  # Render hidden field
                        "</div>"
                    ),
                    css_class="form-group",
                ),
                css_class="panel-body",
            ),
            css_class="panel panel-default",
        )
