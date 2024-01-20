from abc import ABC, abstractmethod
from orderapp.models import Order


class OrderUpdateInterface(ABC):

    @abstractmethod
    def save(self, instance: Order, **kwargs) -> Order:
        """Создание или обновление заказа"""
        pass
