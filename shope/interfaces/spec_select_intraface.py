from abc import ABC, abstractmethod

from django.db.models import QuerySet

from productsapp.models import Specific, Product


class SpecificSelectInterface(ABC):

    @abstractmethod
    def get_specific_by_product(self, product: Product) -> QuerySet[Specific]:
        """ Получить характеристики продукта """
        pass
