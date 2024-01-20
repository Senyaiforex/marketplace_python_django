from django.db.models.signals import post_save
from django.dispatch import receiver

from authapp.models import User
from repositories.cart_repository import RepCart


@receiver(post_save, sender=User)
def create_cart(sender, instance, created, **kwargs):
    """
    Сигнал для создания корзины после создания пользователя
    """
    cart_rep = RepCart()
    if created:
        cart_rep.save(user=instance)
    if not created:
        pass
