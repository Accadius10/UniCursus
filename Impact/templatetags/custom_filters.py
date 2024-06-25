# Impact/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def concat(value, arg):
    """Concatenate value and arg."""
    return str(value) + str(arg)

@register.filter
def add_one(value):
    return value + 1

@register.filter
def equal(value, arg):
    return value == arg