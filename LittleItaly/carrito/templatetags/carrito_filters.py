from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def sum_total(items, attribute):
    try:
        return sum(getattr(item, attribute, 0) for item in items)
    except AttributeError:
        return 0
