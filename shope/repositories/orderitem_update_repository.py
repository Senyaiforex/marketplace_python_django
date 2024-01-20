from interfaces.orderitem_update_interface import OrderItemUpdateInterface
from django.db.models import QuerySet
from orderapp.models import Order, OrderItem
from cartapp.models import CartItem
from repositories.price_repository import PriceRepository

rep_price = PriceRepository()


class OrderItemUpdateRepository(OrderItemUpdateInterface):

    def create_with_cartitems(
            self, order: Order,
            cart_items: QuerySet[CartItem]) -> QuerySet[OrderItem]:
        """Создание позиций в заказе на основании позиций в корзине"""

        order_item_list = list()
        # создание списка объектов OrderItem для bulk_create
        for item in cart_items:
            order_item = OrderItem(
                order=order, product=item.product,
                seller=item.seller, count=item.quantity,
                price=rep_price.get_price(
                    item.product, item.seller) * item.quantity,
                discounted_price=item.discounted_price)

            order_item_list.append(order_item)

        return OrderItem.objects.bulk_create(order_item_list)

    def delete(self, orderitem_id: int) -> None:
        """Удаление позиции из заказа"""
        OrderItem.objects.filter(id=orderitem_id).update(is_active=False)
