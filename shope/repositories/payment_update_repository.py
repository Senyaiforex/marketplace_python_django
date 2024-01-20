from interfaces.payment_update_interface import PaymentUpdateInterface
from paymentapp.models import Payment


class PaymentUpdateRepository(PaymentUpdateInterface):

    def save(self, instance=None, **kwargs) -> Payment:
        """Создание или обновление заказа"""
        if instance:
            payment = instance
            for key in kwargs:
                setattr(payment, key, kwargs[key])
            payment.save()
        else:
            payment = Payment.objects.create(**kwargs)
        return payment
