from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary[key]

@register.filter
def get_dic(dictionary, key):
    return dictionary.get(key)