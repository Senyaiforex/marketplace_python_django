from abc import ABC, abstractmethod
from django.db.models import QuerySet

from authapp.models import User
from orderapp.models import Order


class OrderInterface(ABC):

    @abstractmethod
    def get_all(self) -> QuerySet[Order]:
        pass

    @abstractmethod
    def get_all_by_user(self, user_id):
        """
        Получить все заказы пользователя
        """
        pass

    @abstractmethod
    def get_last_activ(self, user: User) -> QuerySet[Order]:
        pass

    @abstractmethod
    def get_order_by_id(self, order_id: int):
        pass

    @abstractmethod
    def get_orders_by_user_id(self, user_id: int) -> QuerySet[Order]:
        """ Получить все заказы данного юзера """
        pass
