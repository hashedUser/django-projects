from django import template

register = template.Library()

@register.filter(name='remove_whitespace')
def remove_whitespace(value):
    return ''.join(value.split())
