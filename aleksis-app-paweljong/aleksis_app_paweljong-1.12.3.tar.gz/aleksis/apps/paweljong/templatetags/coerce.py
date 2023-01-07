from django import template

register = template.Library()


@register.filter
def coerce_max(value, arg):
    return arg if value > arg else value


@register.filter
def coerce_min(value, arg):
    return arg if value < arg else value
