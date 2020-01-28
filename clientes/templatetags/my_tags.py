from datetime import datetime
from django import template


register = template.Library()

# caso queira passar contexto:
# @register.simple_tag(takes_context=True)


@register.simple_tag()
def current_time(format_string):
    return datetime.now().strftime(format_string)


@register.simple_tag()
def footer_message():
    return "Desenvolvimento web com Django 2.0.2"
