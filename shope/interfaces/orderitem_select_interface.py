from abc import ABC, abstractmethod
from orderapp.models import OrderItem, Order
from django.db.models import QuerySet


class OrderItemSelectInterface(ABC):

    @abstractmethod
    def get_all_items(self, order: Order) -> QuerySet[OrderItem]:
        """ Возвращает все активные позиции в заказе """
        pass
