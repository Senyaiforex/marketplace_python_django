from abc import ABC, abstractmethod
from paymentapp.models import Payment


class PaymentUpdateInterface(ABC):

    @abstractmethod
    def save(self, instance: Payment, **kwargs) -> Payment:
        """Создание или обновление заказа"""
        pass
