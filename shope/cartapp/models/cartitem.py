# flake8: noqa
from django.db import models
from django.utils.translation import gettext_lazy as _
from coreapp.models import BaseModel
from cartapp.models.cart import Cart
from productsapp.models.product import Product
from productsapp.models.seller import Seller


class CartItem(BaseModel):
    """
    CartItems model
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cartitems',
        verbose_name=_('product')
    )
    quantity = models.PositiveIntegerField(
        null=False,
        default=1,
        verbose_name=_('quantity')
    )
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('cart')
    )
    seller = models.ForeignKey(
        Seller,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='seller'
    )
    discounted_price = models.DecimalField(
        default=0,
        verbose_name=_('Discounted price'),
        decimal_places=2,
        max_digits=20

    )

    class Meta:
        verbose_name_plural = _('items in cart')
        verbose_name = _('item in cart')

    def __str__(self):
        return f'{self.product} ({self.quantity})' \

