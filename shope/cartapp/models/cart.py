# flake8: noqa
from django.db import models
from django.utils.translation import gettext_lazy as _
from authapp.models import User
from coreapp.models import BaseModel


class Cart(BaseModel):
    """
    Cart model
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name=_('user'))

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')

    def __str__(self):
        return f'{self.user} cart'
