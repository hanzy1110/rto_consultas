from django.db.models import Q
from django.db.models import Model

import re
from typing import Dict, List, Tuple, Set, Union
from dataclasses import dataclass


@dataclass
class AuxData:
    query_fields: List[str]
    form_fields: Dict[str, Tuple[Union[str, None], Union[Model, None]]]
    parsed_names: Dict[str, str]


def handle_args(query_params, queryset):
    numeric_test = re.compile(r"^\d+$")
    cleaned_query = {k: v for k, v in query_params.items() if v}
    for key, arg in cleaned_query.items():
        if numeric_test.match(str(arg)):
            query = Q(**{f"{key}__exact": int(arg)})
        elif "dominio" in key:
            query = Q(**{f"{key}__exact": arg})
        elif isinstance(arg, str):
            query = Q(**{f"{key}__icontains": arg})
        else:
            return queryset

        queryset = queryset.filter(query)

    return queryset


def handle_query(request, model):
    query = request.GET.copy()
    sort = query.pop("sort", None)
    page = query.pop("page", None)
    queryset = model.objects.all()
    if query:
        queryset = handle_args(query, queryset)
    if sort:
        queryset = queryset.order_by(sort[0])
    return queryset


def handle_form(data: AuxData, model: Model):
    values = {}
    for field in data.form_fields.keys():
        if data.form_fields[field][0]:
            val = model.objects.values_list(field, flat=True).distinct()
            values[field] = val
        else:
            values[field] = [0, 1]
    return values


def map_fields(data: AuxData, model: Model):
    values = {}

    for field, vals in data.form_fields.items():
        dfield, dmodel = vals
        if bool(dfield):
            dfield = vals[0]
            dmodel: Model = vals[1]

            val = model.objects.values_list(field, flat=True).distinct()
            descriptions = dmodel.objects.values_list(dfield, flat=True).distinct()
            values[field] = {v: d for v, d in zip(val, descriptions)}
        else:
            values[field] = {0: "Falso", 1: "Verdadero"}

    return values


def handle_context(context, view):
    val_dict = handle_form(view.aux_data, view.model)
    context["form_fields"] = val_dict
    context["descriptions"] = map_fields(view.aux_data, view.model)
    context["parsed_fields"] = view.aux_data.parsed_names
    fields = view.model._meta.fields
    context["fields"] = fields
    # context["query_fields"] = list(filter(lambda x: x.name in view.query_fields and x.name not in view.form_fields, fields))
    context["query_fields"] = view.aux_data.query_fields
    return context
