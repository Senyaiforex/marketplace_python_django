from interfaces import OrderItemSelectInterface
from orderapp.models import OrderItem, Order
from django.db.models import QuerySet


class OrderItemSelectRepository(OrderItemSelectInterface):

    def get_all_items(self, order: Order) -> QuerySet[OrderItem]:
        """ Возвращает все активные позиции в заказе """

        order_items = OrderItem.objects.filter(order=order, is_active=True)

        return order_items
