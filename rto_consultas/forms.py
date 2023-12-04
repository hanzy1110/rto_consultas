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
    # aux_data = AuxData(
    #     query_fields=[],
    #     form_fields={
    #         "idestado": ("descripcion", Estados),
    #         "idtipouso": ("descripcion", Tipousovehiculo),
    #         "idtipovehiculo": ("descripcion", Tipovehiculo),
    #         "idtaller": ("nombre", Talleres),
    #     },
    #     parsed_names={"name": "name"},
    # )
    # logger.debug(aux_data)
    # vals = map_fields(aux_data, Talleres)
    # logger.debug(vals)

    vals = Talleres.objects.filter(activo__iexact=1).values_list("idtaller", "nombre")
    # choices = list(tuple(vals["idtaller"].items()))
    choices = list(vals)
    a = [("", "")]
    a.extend(choices)
    return a


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


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
                Field(qf, wrapper_class="form-control col-3")
                for qf in form_data.query_fields
            ],
            css_class="form-group row box",
        )
        form_div = Div(
            *[
                Field(ff, wrapper_class="form-control col-3")
                for ff in form_data.form_fields
            ],
            css_class="form-group row box",
        )

        side_by_side = Div(Div(query_div), Div(form_div), css_class="row box")

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


class ResumenMensualForm(forms.Form):
    fecha_desde = forms.DateField(
        required=False,
        label="Fecha Desde",
        widget=forms.DateInput(attrs={"class": "date", "type": "date"}),
    )
    fecha_hasta = forms.DateField(
        required=False,
        label="Fecha Hasta",
        widget=forms.DateInput(attrs={"class": "date", "type": "date"}),
    )
    taller_id = forms.ChoiceField(
        # choices=[("option1", "Option 1"), ("option2", "Option 2")],
        choices=get_choices(),
        required=False,
        label="Planta",
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
                Field("taller_id", wrapper_class="form-group col-6"),
            )
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


ATTRS = "form-control input-sm width:150px;"


class CCCFForm(forms.ModelForm):
    cuit = forms.CharField(label="CUIT", widget=forms.TextInput(attrs={"class": ATTRS}))
    razonsocial = forms.CharField(
        label="Razón Social", widget=forms.TextInput(attrs={"class": ATTRS})
    )
    fechacalibracion = forms.DateField(
        label="Fecha Calibración",
        widget=forms.DateInput(attrs={"class": "date", "type": "date"}),
    )
    fechavencimiento = forms.DateField(
        label="Fecha Vencimiento",
        widget=forms.DateInput(attrs={"class": "date", "type": "date"}),
    )
    desconexioncantidad = forms.IntegerField(
        required=True, label="Cantidad de Desconexiones"
    )  # Example field for 'Cant. Desc.'
    desconexionhora = forms.FloatField(
        required=False,
        label="Hora Desconexión",
        # widget=forms.DateInput(attrs={"class": "date", "type": "datetime-local"}),
    )  # Example field for 'Horas Desc.'
    aperturaequipo = forms.BooleanField(
        required=False, label="Apertura Equipo"
    )  # Example field for 'Apertura Equipo'
    retiroelementograbacion = forms.BooleanField(
        required=False, label="Retiro Elemento Grabación"
    )  # Example field for 'Retiro Elemento Grabación'
    fallasdispositivo = forms.BooleanField(
        required=False, label="Fallas Dispositivo"
    )  # Example field for 'Falla Dispositivo'
    faltainformacion = forms.BooleanField(
        required=False, label="Falta Información"
    )  # Example field for 'Falta Inf.'

    nroinforme = forms.CharField(
        label="Nro Informe",
        widget=forms.TextInput(
            attrs={"class": "form-control input-sm", "id": "txtNroInforme"}
        ),
        required=False,
    )

    canthojas = forms.CharField(
        label="Cant. Hojas/Discos",
        widget=forms.TextInput(
            attrs={"class": "form-control input-sm", "id": "txtCantHojas"}
        ),
        required=False,
    )

    # hfAdjuntos = forms.CharField(
    #     widget=forms.HiddenInput(attrs={"id": "hfAdjuntos"}),
    #     required=False,
    # )

    cccf_files = MultipleFileField(label="Carga Archivos", required=False)

    class Meta:
        model = CccfCertificados
        # fields = "__all__"
        exclude = (
            "cb",
            "idtaller",
            "idempresa",
            "fechahoracarga",
            "idestado",
            "patentemercosur",
        )

    def __init__(self, *args, **kwargs):
        super(CCCFForm, self).__init__(*args, **kwargs)

        # logger.debug(f"FORM FIELDS => {self.fields}")

        # for f in self.files.keys():
        #     self.files[f].widget.attrs.update({"class": "form-control input-sm"})
        # for field_name, field in self.fields.items():
        #     field.required = False

        self.helper = FormHelper()
        self.helper.form_id = "formCargaCert"
        self.helper.form_method = "post"
        self.helper.form_class = "form-horizontal"
        # self.helper.form_enctype = "multipart/form-data"

        self.helper.layout = Layout(
            Div(
                Div(
                    HTML("<h2>Datos del Certificado</h2>"),
                    Div(
                        Field("nrocertificado", wrapper_class="form-group col-4"),
                        Field("fechacalibracion", wrapper_class="form-group col-4"),
                        Field("fechavencimiento", wrapper_class="form-group col-4"),
                        css_class="form-group row box",
                    ),
                    css_class="card card-plain mt-2 box",
                    # template="forms/cccf_layout.html",
                ),
                Div(
                    HTML("<h2>Datos del Propietario</h2>"),
                    Div(
                        Field("cuit", wrapper_class="form-group col-4"),
                        Field("razonsocial", wrapper_class="form-group col-4"),
                        Field("usuario", wrapper_class="form-group col-4"),
                        css_class="form-group row box",
                    ),
                    css_class="card card-plain mt-2 box",
                ),
                Div(
                    HTML("<h2>Datos del Vehículo</h2>"),
                    Div(
                        Field("dominio", wrapper_class="form-group col-4"),
                        Field("nrointerno", wrapper_class="form-group col-4"),
                        Field("kilometraje", wrapper_class="form-group col-4"),
                        css_class="form-group row box",
                    ),
                    css_class="card card-plain mt-2 box",
                ),
                Div(
                    HTML("<h2>Datos del Tacógrafo</h2>"),
                    Div(
                        Field("tacmarca", wrapper_class="form-group col-6"),
                        Field("tactipo", wrapper_class="form-group col-6"),
                        Field("tacmodelo", wrapper_class="form-group col-6"),
                        Field("tacnroserie", wrapper_class="form-group col-6"),
                        Field("relw", wrapper_class="form-group col-6"),
                        Field("constantek", wrapper_class="form-group col-6"),
                        Field("rodado", wrapper_class="form-group col-6"),
                        Field("precinto", wrapper_class="form-group col-6"),
                        Field("impresora", wrapper_class="form-group col-6"),
                        Field("observaciones", wrapper_class="form-group col-6"),
                        css_class="form-group row box",
                    ),
                    css_class="card card-plain mt-2 box",
                ),
                Div(
                    HTML("<h2>Información</h2>"),
                    Div(
                        Field("desconexioncantidad", wrapper_class="form-group col-6"),
                        Field("desconexionhora", wrapper_class="form-group col-6"),
                        css_class="form-group row box",
                    ),
                    css_class="card card-plain mt-2 box",
                ),
                Div(
                    Div(
                        Field("aperturaequipo"),
                        Field("retiroelementograbacion"),
                        Field("fallasdispositivo"),
                        Field("faltainformacion"),
                        css_class="form-group row box",
                    ),
                    css_class="card card-plain mt-2 box",
                ),
                Div(
                    Div(
                        Field("nroinforme", wrapper_class="col-6"),
                        Field("canthojas", wrapper_class="col-6"),
                        Field("cccf_files"),
                        css_class="form-group row box",
                    ),
                    css_class="card card-plain mt-2 box",
                ),
            )
        )
