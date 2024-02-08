import os
import re
import types
from django import template
from django.utils.html import escape
from django.core.exceptions import ImproperlyConfigured
from django.template import Node
from django.utils.http import urlencode

# import rto_consultas.models as models

# from rto_consultas.logging import configure_logger
# LOG_FILE = os.environ["LOG_FILE"]
# logger = configure_logger(LOG_FILE)

context_processor_error_msg = (
    "Tag {%% %s %%} requires django.template.context_processors.request to be "
    "in the template configuration in "
    "settings.TEMPLATES[]OPTIONS.context_processors) in order for the included "
    "template tags to function correctly."
)
numeric_test = re.compile("^\d+$")
register = template.Library()


@register.filter(name="getattr")
def get_attr(object, arg):
    if hasattr(object, str(arg)):
        attr = getattr(object, arg)
        if type(getattr(object, str(arg))) == types.MethodType:
            return attr()
        return attr
    elif hasattr(object, "has_key"):
        try:
            if object.has_key(arg):
                return object[arg]
        except Exception as e:
            print(e)
            return object.filter(**{f"{arg}": arg})

    elif numeric_test.match(str(arg)) and len(object) > int(arg):
        return object[int(arg)]
    else:
        return object


@register.simple_tag(takes_context=True)
def get_model_attr(context, instance, name):
    return get_attr(instance, name)


@register.simple_tag(takes_context=True)
def get_reverificados_cant(context, cat):
    try:
        return context["reverificados"][cat]["cantidad"]
    except Exception as e:
        print(e)
        return "RENDER ERROR"


@register.simple_tag(takes_context=True)
def get_reverificados_value(context, cat):
    try:
        return context["reverificados"][cat]["values"]
    except Exception as e:
        print(e)
        return "RENDER ERROR"


@register.simple_tag(takes_context=True)
def query_dict(context, instance, name):
    if isinstance(name, str):
        name = name.replace(" ", "")
    try:
        return instance[name]
    except KeyError:
        return "Unknown!!"


@register.simple_tag(takes_context=True)
def query_descriptions(context, descriptions, field, value):
    # try:
    return descriptions[field][value]
    # except KeyError as e:
    #     print(e)
    #     raise KeyError
    #     # return "Desconocido"


@register.simple_tag(takes_context=True)
def get_by_name(context, name):
    """ "Get variable by string name {% get_by_name data_name.data_func... %}"""
    print(context["instance"].get_edit_url())
    arr = name.split(".")
    obj = arr[0]
    object = context[obj]
    if len(arr) > 1:
        for ar in arr:
            object = get_attr(object, ar)
    return object


class QuerystringNode(Node):
    def __init__(self, updates, removals, asvar=None):
        super().__init__()
        self.updates = updates
        self.removals = removals
        self.asvar = asvar

    def render(self, context):
        if "request" not in context:
            raise ImproperlyConfigured(context_processor_error_msg % "querystring")

        params = dict(context["request"].GET)
        for key, value in self.updates.items():
            if isinstance(key, str):
                params[key] = value
                continue
            key = key.resolve(context)
            value = value.resolve(context)
            if key not in ("", None):
                params[key] = value
        for removal in self.removals:
            params.pop(removal.resolve(context), None)

        value = escape("?" + urlencode(params, doseq=True))

        if self.asvar:
            context[str(self.asvar)] = value
            return ""
        else:
            return value


@register.simple_tag(takes_context=True)
def export_url_custom(context, export_format, export_trigger_param=None):
    """
    Returns an export URL for the given file `export_format`, preserving current
    query string parameters.

    Example for a page requested with querystring ``?q=blue``::

        {% export_url "csv" %}

    It will return::

        ?q=blue&amp;_export=csv
    """

    if export_trigger_param is None and "view" in context:
        export_trigger_param = getattr(context["view"], "export_trigger_param", None)

    export_trigger_param = export_trigger_param or "_export"

    query_string_node = QuerystringNode(
        updates={export_trigger_param: export_format}, removals=[]
    ).render(context)

    # logger.info(f"QUERY STRING RETURNED ===> {query_string_node}")
    # parse the querystring from the url and use the correct one!!!
    return query_string_node


@register.simple_tag(takes_context=True)
def check_anulado(context):
    return context["certificado"]["anulado"] == 1


@register.simple_tag(takes_context=True)
def filter_idestado(context, verifs, estado):
    return verifs.filter(idestado=estado)


@register.simple_tag(takes_context=True)
def translate(context, name):
    match name:
        case "Username":
            return "Usuario"
        case "Password":
            return "Contraseña"
        case _:
            return name


@register.filter(takes_context=True)
def parse_none(value):
    match value:
        case None:
            return ""
        case "NULL":
            return ""
        case _:
            return value
