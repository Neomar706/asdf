from django import template
from django.utils.html import urlize
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def description_format(value):
    text = urlize(value)
    text = text.replace('\n', '<br>')
    text = text.replace('<a ', '<a target="_blank" class="text-blue-400" ')
    text = mark_safe(text)
    return text

register.filter('description_format', description_format)