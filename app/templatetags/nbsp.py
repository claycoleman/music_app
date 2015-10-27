# app/templatetags/nbsp.py

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name="nbsp")
def nbsp(value):
    return mark_safe("&nbsp;".join(value.split(' ')))