from django.db import models
from coreapp.models import BaseModel
from taggit.managers import TaggableManager

from .category import Category
from django.utils.translation import gettext_lazy as _


class Product(BaseModel):
    """
    Класс модель для продуктов
    """
    name = models.CharField(verbose_name=_("name"),
                            max_length=100)
    description = models.TextField(verbose_name=_("description"),
                                   null=False,
                                   blank=True)
    short_description = models.TextField(verbose_name=_("short_description"),
                                         null=True,
                                         blank=True,
                                         max_length=100)
    tags = TaggableManager()
    archived = models.BooleanField(default=False,
                                   verbose_name=_("archived"))
    free_delivery = models.BooleanField(default=False,
                                        verbose_name=_("free_delivery"))
    category = models.ForeignKey(
        Category,
        on_delete=models.DO_NOTHING,
        verbose_name=_('category'),
        related_name='category_products'
    )

    is_limited = models.BooleanField(
        default=False,
        verbose_name=_('limited')
    )

    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")

    def __str__(self):
        return self.name

    def get_all_tags(self) -> str:
        """ Метод для получения всех тегов продукта """
        return ", ".join(
            [str(tag) for tag in self.tags.all()]
        )
