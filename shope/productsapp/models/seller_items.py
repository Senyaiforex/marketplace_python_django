from django.db import models

from coreapp.models import BaseModel
from productsapp.models import Seller, Product
from django.utils.translation import gettext_lazy as _


class SellerItem(BaseModel):
    """
    Класс-модель товара у продавца
    """
    seller = models.ForeignKey(
        Seller,
        on_delete=models.CASCADE,
        related_name='seller_items',
        verbose_name=_('seller')
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='seller_items',
        verbose_name=_('product')
    )

    def __str__(self):
        return f'{self.seller} {self.product} '

    class Meta:
        verbose_name = _("seller's item")
        verbose_name_plural = _("seller's items")
