import re
import types
from django import template

import rto_consultas.models as models

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
def query_dict(context, instance, name):
    if isinstance(name, str):
        name = name.replace(" ", "")
    try:
        return instance[name]
    except KeyError:
        return "Unknown!!"


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


@register.simple_tag(takes_context=True)
def get_categorias(context, idcategoria):
    return models.Categorias.objects.get(idcategoria__exact=idcategoria).descripcion


@register.simple_tag(takes_context=True)
def get_certificado_url(context):
    pass


@register.simple_tag(takes_context=True)
def get_tarjeta_verde_url(context):
    pass


@register.simple_tag(takes_context=True)
def get_lista_defectos(context):
    pass


@register.simple_tag(takes_context=True)
def get_pa_style(context):
    pass


@register.simple_tag(takes_context=True)
def get_ca_style(context):
    pass


@register.simple_tag(takes_context=True)
def get_TCa_style(context):
    pass


@register.simple_tag(takes_context=True)
def get_tm_style(context):
    pass


@register.simple_tag(takes_context=True)
def check_anulado(context):
    return context["certificado"]["anulado"] == 1


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
