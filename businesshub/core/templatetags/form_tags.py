from django import template

register = template.Library()


@register.filter(name="add_attr")
def add_attr(field, attr):
    attrs = {}
    definition = attr.split("=")
    if len(definition) == 2:
        attrs[definition[0]] = definition[1]
    else:
        attrs[definition[0]] = True
    return field.as_widget(attrs=attrs)
