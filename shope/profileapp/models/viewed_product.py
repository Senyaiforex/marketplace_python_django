from django.db import models
from authapp.models import User
from productsapp.models import Product
from coreapp.models import BaseModel
from django.utils.translation import gettext_lazy as _


class ViewedProduct(BaseModel):
    """
    Model for viewed product
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='viewed_products',
        verbose_name=_('user')
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='viewed_by_users'
    )

    def __str__(self):
        return f'{self.user} - {self.product}'

    class Meta:
        verbose_name = _('viewed product')
        verbose_name_plural = _('viewed products')
