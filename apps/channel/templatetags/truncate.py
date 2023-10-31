from django import template


register = template.Library()


@register.filter
def truncate(value, length):

    if len(value) <= length:
        return value

    truncated_text = value[:length]
    last_space_index = truncated_text.rfind(' ')

    if last_space_index != -1:
        truncated_text = truncated_text[:last_space_index]
    
    return truncated_text + '...'

register.filter('truncate', truncate)