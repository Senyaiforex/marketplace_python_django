from django.db import models
from coreapp.models import BaseModel

from productsapp.models.product import Product
from profileapp.models import Profile
from django.utils.translation import gettext_lazy as _


class Review(BaseModel):
    """
    Класс-модель для комментариев
    """
    user = models.ForeignKey(Profile,
                             on_delete=models.CASCADE,
                             related_name="reviews")
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name="reviews")
    text = models.TextField(blank=True,
                            null=False,
                            verbose_name=_("text"))

    class Meta:
        verbose_name = _("review")
        verbose_name_plural = _("reviews")

    def __str__(self):
        return f"{_('Reviews from')} {self.user.user.first_name}"
