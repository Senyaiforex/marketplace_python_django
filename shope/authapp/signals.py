from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.db import transaction

from authapp.models import User


@receiver(post_save, sender=User)
def add_to_sellers_group(sender, instance, created, **kwargs):
    if instance.is_staff and not instance.is_superuser:
        sellers_group = Group.objects.get(name='Продавцы')
        sellers_group.user_set.add(instance)
        transaction.on_commit(lambda: instance.groups.set([sellers_group],
                                                          clear=True))
    else:
        transaction.on_commit(lambda: instance.groups.set([],
                                                          clear=True))
