from django import template

register = template.Library()

@register.filter
def snakeToSpace(value):
    """Converts _ to Space"""
    return value.replace('_',' ')

@register.filter
def snakeToTitle(value):
    """Converts snake_case variable to title variable 'Snake Case'"""
    return value.replace('_', ' ').lower().title()
