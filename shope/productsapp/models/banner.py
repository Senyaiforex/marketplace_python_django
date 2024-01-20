from django.db import models
from coreapp.models import BaseModel
from productsapp.models import Category
from django.utils.translation import gettext_lazy as _


class Banner(BaseModel):
    """
    Класс-модель баннеров на главной странице
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name=_('category'),
        related_name='category_on_banner'
    )

    image = models.ImageField(
        upload_to='banners_images/',
        verbose_name=_('image')
    )

    class Meta:
        verbose_name = _("banner")
        verbose_name_plural = _("banners")

    def __str__(self):
        return self.category.name

    @property
    def category_min_price(self):
        return None
