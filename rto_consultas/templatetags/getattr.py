import re
import types
from django import template

numeric_test = re.compile("^\d+$")
register = template.Library()

@register.filter(name="getattr")
def get_attr(object, arg):
    if hasattr(object, str(arg)):
        attr = getattr(object, arg)
        if type(getattr(object, str(arg))) == types.MethodType:
            return attr()
        return attr
    elif hasattr(object, 'has_key'):
        try:
            if object.has_key(arg):
                return object[arg]
        except Exception as e:
            print(e)
            return object.filter(**{f"{arg}":arg})

    elif numeric_test.match(str(arg)) and len(object) > int(arg):
        return object[int(arg)]
    else:
        return object

@register.simple_tag(takes_context=True)
def get_model_attr(context, instance, name):
    return get_attr(instance, name)

@register.simple_tag(takes_context=True)
def query_dict(context, instance, name):
    try:
        return instance[name]
    except KeyError:
        return "Unknown!!"

@register.simple_tag(takes_context=True)
def query_descriptions(context, descriptions, field, value):
    try:
        return descriptions[1][field][value]
    except KeyError as e:
        print(e)
        return "Desconocido"
        

@register.simple_tag(takes_context=True)
def get_by_name(context, name):
    """"Get variable by string name {% get_by_name data_name.data_func... %}"""
    print(context['instance'].get_edit_url())
    arr = name.split('.')
    obj = arr[0]
    object = context[obj]
    if len(arr) > 1:
        for ar in arr:
            object = get_attr(object, ar)
    return object

