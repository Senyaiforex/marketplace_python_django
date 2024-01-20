from django import template
import re

register = template.Library()


@register.filter(name="sortclass")
def sortclass(value, arg):
    """Модификатор CSS-класса для кнопки сортировки"""
    if value == arg:
        return 'Sort-sortBy_inc'
    elif value == ('-' + arg):
        return 'Sort-sortBy_dec'


@register.filter(name="sortquery")
def sortquery(path, mode):
    """Формирует URL для кнопки сортировки"""
    new_sort = f'&sort={mode}'
    last_sort = re.search(r'(&?sort=.*&)|(&?sort=.*$)', path)
    if last_sort:
        if last_sort.group() == new_sort:
            new_sort = f'&sort=-{mode}'
    result = re.sub(r'(&?sort=.*(?=&))|(&?sort=.*$)', '', path)
    return result + new_sort
