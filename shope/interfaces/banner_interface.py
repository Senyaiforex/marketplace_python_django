from abc import ABC, abstractmethod
from django.db.models import QuerySet
from productsapp.models import Banner


class BannerInterface(ABC):

    @abstractmethod
    def get_all(self) -> QuerySet[Banner]:
        """ Метод получения всех баннеров"""
        pass

    @abstractmethod
    def get_random_banners(self, quantity: int = 3) -> QuerySet[Banner]:
        """
        Метод получения случайных баннеров в определенном количестве,
        по-умолчанию - 3.
        """
        pass
