from django.db import models
from coreapp.models import BaseModel
from productsapp.models.product import Product, Category
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator


class BaseDiscount(BaseModel):
    """ Базовый абстрактный класс модели скидок """
    name = models.CharField(
        max_length=50,
        blank=True,
        null=False,
        verbose_name=_('name'))
    value = models.DecimalField(
        null=True,
        max_digits=4,
        decimal_places=2,
        verbose_name=_('value'))
    start_date = models.DateField(
        null=False,
        blank=True,
        verbose_name=_('start date'))
    expiration_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('expiration date'))
    description = models.CharField(
        max_length=200,
        blank=True,
        null=False,
        verbose_name=_('description'))
    priority = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        validators=[MaxValueValidator(10)],
        verbose_name=_('priority'))

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.name} - {self.value} - {self.priority}'


class SetDiscount(BaseDiscount):
    """ Класс-модель скидки на фиксированный набор продуктов """
    products = models.ManyToManyField(
        Product,
        related_name='set_discounts',
        verbose_name=_('products'))

    class Meta:
        verbose_name = _("Set Discount")
        verbose_name_plural = _("Set Discounts")


class ProductDiscount(BaseDiscount):
    """ Класс-модель скидки для списка продуктов и/или категорий"""
    products = models.ManyToManyField(
        Product,
        related_name='product_discounts',
        verbose_name=_('products'),
        blank=True,
        default=None)
    categories = models.ManyToManyField(
        Category,
        related_name='category_discounts',
        verbose_name=_('categories'),
        blank=True,
        default=None)

    class Meta:
        verbose_name = _("Product Discount")
        verbose_name_plural = _("Product Discounts")


class CartDiscount(BaseDiscount):
    """Класс-модель скидки на корзину товаров"""
    required_sum = models.DecimalField(
        default=None,
        blank=True,
        null=True,
        max_digits=10,
        decimal_places=2,
        verbose_name=_('required sum'))
    required_quantity = models.PositiveSmallIntegerField(
        default=None,
        blank=True,
        null=True,
        verbose_name=_('required quantity'))

    class Meta:
        verbose_name = _("Cart Discount")
        verbose_name_plural = _("Cart Discounts")
