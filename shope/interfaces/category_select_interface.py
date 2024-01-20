from abc import ABC, abstractmethod
from django.db.models import QuerySet
from productsapp.models.category import Category


class CategorySelectInterface(ABC):

    @abstractmethod
    def non_empty_categories(self) -> QuerySet[Category]:
        """Получить список всех категорий, в которых есть товары"""
        pass
