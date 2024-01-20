from django.db import models
from coreapp.models import BaseModel
from django.utils.translation import gettext_lazy as _


class Category(BaseModel):
    """
    Класс-модель для определения категории продукта
    """
    name = models.CharField(max_length=100,
                            null=False,
                            blank=True,
                            verbose_name=_("name"))

    icon = models.FileField(
        upload_to='categories_icons/',
        null=True,
        blank=True,
        verbose_name=_('icon (SVG)'))

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name
