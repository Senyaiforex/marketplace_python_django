from abc import ABC, abstractmethod

from django.db.models import QuerySet

from productsapp.models import Product, Seller


class SellerSelectInterface(ABC):

    @abstractmethod
    def get_all_sellers(self) -> QuerySet[Seller]:
        """ Получить всех продавцов """
        pass

    @abstractmethod
    def get_seller_by_product(self, product: Product) -> QuerySet[Seller]:
        """ Получить продавцов с определенным продуктом """
        pass

    @abstractmethod
    def get_sellers_count(self) -> int:
        """ Получить количество продавцов """
        pass
