from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    """
    Класс базовой модели
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class ConfigModel(models.Model):
    """
    Класс модели для настроек
    """
    name = models.CharField(
        max_length=100,
        null=False,
        blank=True,
        verbose_name=_('name')
    )

    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('value')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Base configuration")
        verbose_name_plural = _("Base configurations")
