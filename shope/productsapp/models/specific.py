from django.db import models
from coreapp.models import BaseModel
from .product import Product
from .type_spec import TypeSpecific
from django.utils.translation import gettext_lazy as _


class Specific(BaseModel):
    """
    Класс-модель для характеристики продукта
    """
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name="specific")
    description = models.TextField(null=True,
                                   blank=True,
                                   verbose_name=_("description"))
    type_spec = models.ForeignKey(TypeSpecific,
                                  on_delete=models.CASCADE,
                                  related_name="specific")

    def __str__(self):
        return f'{self.type_spec.name} - {self.description}'
