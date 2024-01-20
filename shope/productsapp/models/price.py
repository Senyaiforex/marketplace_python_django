from django.db import models

from coreapp.models import BaseModel
from productsapp.models import Product, Seller
from django.utils.translation import gettext_lazy as _


class SlicePrice(BaseModel):
    """
    Класс-модель для цены
    """
    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('value')
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_price',
        verbose_name=_('product')
    )

    seller = models.ForeignKey(
        Seller,
        on_delete=models.CASCADE,
        related_name='slice_price',
        verbose_name=_('seller')
    )

    def __str__(self):
        return f"{self.product.name} - {self.seller.name} - {self.value}"

    class Meta:
        verbose_name = _("price slice")
        verbose_name_plural = _("price slices")
