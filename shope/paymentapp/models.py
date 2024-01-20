from coreapp.models import BaseModel
from django.db import models
from authapp.models import User
from coreapp.enums import PAYMENT_STATUSES
from django.utils.translation import gettext_lazy as _

from orderapp.models import Order


class Payment(BaseModel):
    """
    Класс-модель платежа
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('user'))
    payment_id = models.CharField(
        max_length=100,
        verbose_name=_('yookassa payment id'))
    amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name=_('amount'))
    status = models.CharField(
        max_length=20,
        verbose_name=_('payment status'),
        choices=PAYMENT_STATUSES)

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name=_('order'),
        related_name='payment'
    )

    def __str__(self):
        return self.payment_id

    class Meta:
        verbose_name = _('payment')
        verbose_name_plural = _('payments')


class Card(BaseModel):
    """
    Класс-модель платежной карты
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('user'))
    number = models.CharField(
        max_length=20,
        verbose_name=_('card number'))
    payment_method_id = models.CharField(
        max_length=100,
        verbose_name=_('payment method id'))
    card_type = models.CharField(
        max_length=10,
        verbose_name=_('card type'))
    expiration_date = models.DateField(
        verbose_name=_('expiration date'))

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = _('card')
        verbose_name_plural = _('cards')
