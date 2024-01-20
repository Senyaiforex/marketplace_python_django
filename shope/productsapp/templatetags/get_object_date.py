from django import template
from datetime import datetime

register = template.Library()


@register.simple_tag()
def get_object_date(date_string):
    """Возвращает объект datetime из строки"""
    date_object = datetime.strptime(date_string, "%b-%d-%Y")
    return date_object
