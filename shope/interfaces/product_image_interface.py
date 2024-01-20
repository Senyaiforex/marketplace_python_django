from abc import ABC, abstractmethod
from django.db.models import QuerySet

from productsapp.models import Product
from productsapp.models.images import ProductImage


class ProductImageInterface(ABC):

    @abstractmethod
    def get_all_images(self, product: Product) -> QuerySet[ProductImage]:
        """Получить все изображения данного продукта"""
        pass
