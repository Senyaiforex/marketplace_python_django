from django.db import models

from coreapp.models import BaseModel
from productsapp.models import Product
from django.utils.translation import gettext_lazy as _


class ProductImage(BaseModel):
    """
    Класс-модель для картинок продукта
    """
    image = models.ImageField(
        upload_to='products_images/',
        verbose_name=_('image')
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_images',
        verbose_name=_('product')
    )

    def __str__(self):
        return f"{self.product.name} - {self.image.name}"

    class Meta:
        verbose_name = _("product image")
        verbose_name_plural = _("product images")
