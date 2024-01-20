from django import template
from repositories.price_repository import PriceRepository

rep_price = PriceRepository()
register = template.Library()


@register.simple_tag()
def get_price(price, quantity):
    """Возвращает цену на товар в корзине
    с учётом его количества"""
    return price * quantity
