from django import template
from repositories import PriceRepository
from coreapp.utils import ProductDiscounts

register = template.Library()
price_rep = PriceRepository()
disc_util = ProductDiscounts()


@register.simple_tag()
def get_price_a_seller(product, seller):
    """Возвращает цену,
    установленную продавцом на товар
    """
    price = price_rep.get_price(product, seller)
    discount = disc_util.get_priority_product_discount(product,
                                                       product.category)
    if discount:
        price = round(price * (1 - discount.value / 100), 2)
    return price
