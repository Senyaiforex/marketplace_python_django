from abc import ABC, abstractmethod
from productsapp.models import Product, Category, \
    SetDiscount, ProductDiscount, CartDiscount

from django.db.models import QuerySet


class DiscountInterface(ABC):
    """
    Интерфейс для работы со скидками
    """

    @abstractmethod
    def get_discount_by_product_or_category(self, product: Product,
                                            category: Category) \
            -> ProductDiscount:
        """
        Метод получения скидки на товар
        """
        pass

    @abstractmethod
    def get_discount_by_cart(self) -> CartDiscount:
        """
        Метод получения скидки на корзину
        """
        pass

    @abstractmethod
    def get_set_discounts_for_product(
            self, product: Product) -> QuerySet[SetDiscount]:
        """
        Получить все скидки на наборы, в которых есть данный продукт
        """
        pass

    @abstractmethod
    def get_set_discounts_all(self) -> QuerySet[SetDiscount]:
        """
        Получить все скидки на наборы, которые
        действуют сейчас или будет действовать
        в будущем
        """
        pass

    @abstractmethod
    def get_cart_discounts_all(self) -> QuerySet[CartDiscount]:
        """
        Получить все скидки на корзину, которые
        действуют сейчас или будет действовать
        в будущем
        """
        pass

    @abstractmethod
    def get_products_discounts_all(self) -> QuerySet[ProductDiscount]:
        """
        Получить все скидки на товары, которые
        действуют сейчас или будет действовать
        в будущем
        """
        pass

    @abstractmethod
    def get_product_with_discount(self):
        """
        Получить товары с активными скидками
        """
        pass

    @abstractmethod
    def get_set_discount_by_id(self, set_id: int) -> SetDiscount:
        """
        Получить набор скидок на товар по id
        :param set_id: id объекта SetDiscount
        :return: объект SetDiscount
        """
        pass

    @abstractmethod
    def get_cart_discount_by_id(self, cart_id: int) -> CartDiscount:
        """
        Получить скидку на корзину по id
        :param cart_id: id объекта CartDiscount
        :return: объект CartDiscount
        """
