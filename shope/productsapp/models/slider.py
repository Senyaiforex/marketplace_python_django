from django.db import models
from coreapp.models import BaseModel
from productsapp.models import Product
from django.utils.translation import gettext_lazy as _


class Slider(BaseModel):
    """
    Класс-модель слайдера на главной странице
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('product'),
        related_name='product_on_slider'
    )

    description = models.CharField(
        max_length=300,
        verbose_name=_('description')
    )

    class Meta:
        verbose_name = _("slider")
        verbose_name_plural = _("sliders")

    def __str__(self):
        return self.product.name
