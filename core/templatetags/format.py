from django import template
register = template.Library()

@register.filter
def format_importo(value):
    try:
        if value == 0 or value == 0.0:
            return ""
        return "{:,.2f}".format(value).replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return value