from django import template
from datetime import timedelta


register = template.Library()


@register.filter
def durationformat(value):
    duration: timedelta = value
    seconds = duration.seconds % 60
    minutes = duration.seconds // 60
    hours   = minutes // 60

    return '{0}{1}{2}'.format(str(hours) + ':' if hours >= 1 else '', 
                              str(minutes) + ':' if minutes >= 1 else '', 
                              seconds)
    

register.filter('durationformat', durationformat)