from django.db.models.signals import post_save
from django.dispatch import receiver

from authapp.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        fio = f'{instance.first_name} ' \
              f'{instance.middle_name} ' \
              f'{instance.last_name}'
        Profile.objects.create(
            user=instance,
            fio=fio
        )
    if not created:
        pass
