from django import template
register = template.Library()

@register.filter
def format_importo(value):
    try:
        return "{:,.2f}".format(value).replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return value