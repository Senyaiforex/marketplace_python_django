from django import template
from coreapp.utils import ProductDiscounts

register = template.Library()
disc_util = ProductDiscounts()


@register.filter(name="discounted_price")
def discounted_price(product, price):
    """
    Возвращает цену со скидкой на товар
    """
    discount = disc_util.get_priority_product_discount(product,
                                                       product.category)
    if discount:
        return round(price * (1 - discount.value / 100), 2)
    else:
        return None
