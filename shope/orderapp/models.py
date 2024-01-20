from django.db import models
from coreapp.models import BaseModel
from authapp.models import User
from productsapp.models import Seller, Product
from coreapp.enums import ORDER_STATUSES, DELIVERY_TYPE, \
    DEFAULT, NOT_PAID_STATUS
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class Order(BaseModel):
    """
    Класс модели заказа
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        related_name='orders'
    )

    fio = models.CharField(
        max_length=100,
        verbose_name=_('FIO')
    )

    phone_number = PhoneNumberField(
        blank=True,
        verbose_name=_('phone number')
    )

    status = models.CharField(
        max_length=20,
        verbose_name=_('status'),
        choices=ORDER_STATUSES,
        default=NOT_PAID_STATUS
    )

    city = models.CharField(
        max_length=50,
        verbose_name=_('city'),
    )

    address = models.CharField(
        max_length=100,
        verbose_name=_('address')
    )

    delivery_type = models.CharField(
        max_length=20,
        verbose_name=_('delivery type'),
        choices=DELIVERY_TYPE,
        default=DEFAULT
    )

    delivery_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name=_('delivery price')
    )

    total_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name=_('total price')
    )

    total_discounted_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name=_('total discounted price')
    )

    def __str__(self):
        return f'Order {self.id}'

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')


class OrderItem(BaseModel):
    """
    Класс модели товара в заказе
    """
    order = models.ForeignKey(
        Order,
        related_name='order_items',
        on_delete=models.CASCADE,
        verbose_name=_('order')
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('product'),
        related_name='ordered'
    )

    count = models.PositiveSmallIntegerField(
        verbose_name=_('count')
    )

    seller = models.ForeignKey(
        Seller,
        on_delete=models.CASCADE,
        verbose_name=_('seller')
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name=_('price'))

    discounted_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name=_('discounted price'))

    def __str__(self):
        return f'{self.product} x{self.count}'

    class Meta:
        verbose_name = _('order item')
        verbose_name_plural = _('order items')
