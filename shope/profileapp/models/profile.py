from django.db import models
from authapp.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    """
    Profile models.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('user')
    )
    fio = models.CharField(
        max_length=100,
        verbose_name=_('FIO')
    )

    avatar_image = models.ImageField(
        upload_to='profile_avatars/',
        verbose_name=_('avatar'),
        null=True,
        blank=True,
    )

    phone_number = PhoneNumberField(
        blank=True,
        verbose_name=_('phone number')
    )

    def __str__(self):
        return f'{self.fio} - {self.user.email}'

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')
