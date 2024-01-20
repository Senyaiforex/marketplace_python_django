from django.db.models import QuerySet
from django.http import HttpRequest

from productsapp.models import Product
from repositories.product_select_repository import ProductSelectRepository


_repository = ProductSelectRepository()


class ProductsComparisonList:
    """
    Сервис сравнения товаров
    """

    @classmethod
    def add_to_comparison(cls, request: HttpRequest, product_id: int) -> None:
        """
        Добавить товар в список сравнения

        :param request: запрос
        :param product_id: id товара, добавляемого в список сравнения

        :return: None
        """
        comparison_list: list = request.session.get("comparison_list", [])
        if product_id not in comparison_list:
            if len(comparison_list) >= 2:
                different = len(comparison_list) - 2
                comparison_list = comparison_list[different + 1:]
            comparison_list.append(product_id)
        request.session["comparison_list"] = comparison_list

    @classmethod
    def remove_from_comparison(cls,
                               request: HttpRequest,
                               product_id: int) -> None:
        """
        Убрать товар из списка сравнения

        :param request: запрос
        :param product_id: id товара, который надо убрать из списка сравнения

        :return: None
        """
        if product_id in request.session["comparison_list"]:
            products = request.session["comparison_list"]
            products.remove(product_id)
            request.session["comparison_list"] = products

    @staticmethod
    def get_comparison_list(request: HttpRequest,
                            count: int = 3) -> QuerySet[Product]:
        """
        Получение списка товаров, добавленных к сравнению (с возможностью
        ограничить количество, по умолчанию максимум — три первых)

        :param request: запрос

        :param count: количество товаров
        :return: QuerySet[Product]
        """
        products_id = request.session.get("comparison_list") or []
        products_id = products_id[:count + 1] if count < len(products_id) \
            else products_id
        return _repository.get_products_with_these_id(products_id)

    @classmethod
    def comparison_list_size(cls, request: HttpRequest) -> int:
        """
        Получение количества товаров в списке сравнения

        :param request: запрос
        :return: int
        """
        return len(request.session.get("comparison_list", []))
