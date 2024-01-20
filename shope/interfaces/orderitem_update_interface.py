from abc import ABC, abstractmethod
from django.db.models import QuerySet
from orderapp.models import Order, OrderItem
from cartapp.models import CartItem


class OrderItemUpdateInterface(ABC):

    @abstractmethod
    def create_with_cartitems(
            self, order: Order,
            cart_items: QuerySet[CartItem]) -> QuerySet[OrderItem]:
        """Создание позиций в заказе на основании позиций в корзине"""
        pass

    @abstractmethod
    def delete(self, orderitem_id: int) -> None:
        """Удаление позиции из заказа"""
        pass
