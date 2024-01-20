from abc import ABC, abstractmethod

from django.db.models import QuerySet

from productsapp.models import Product, Review


class ReviewInterface(ABC):

    @abstractmethod
    def get_all_reviews(self, product: Product) -> QuerySet[Review]:
        """ Получить все отзывы к продукту """
        pass

    @abstractmethod
    def get_amount_reviews(self, product: Product) -> int:
        """ Получить количество отзывов к продукту """
        pass

    @abstractmethod
    def save(self, review: Review, force=None) -> None:
        """ Обновление или создание отзыва """
        pass
