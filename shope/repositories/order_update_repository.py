from interfaces.order_update_interface import OrderUpdateInterface
from orderapp.models import Order


class OrderUpdateRepository(OrderUpdateInterface):

    def save(self, instance=None, **kwargs) -> Order:
        """Создание или обновление заказа"""
        if instance:
            order = instance
            for key in kwargs:
                setattr(order, key, kwargs[key])
            order.save()
        else:
            order = Order.objects.create(**kwargs)
        return order
