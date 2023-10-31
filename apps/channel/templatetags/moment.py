from django import template
from django.utils import timezone



register = template.Library()

@register.filter
def custom_naturaltime(value):
    now = timezone.now()
    delta = now - value

    if delta.days == 0:
        return 'hoy'
    elif delta.days == 1:
        return 'ayer'
    else:
        return f'hace {delta.days} días'



register.filter('custom_naturaltime', custom_naturaltime)

