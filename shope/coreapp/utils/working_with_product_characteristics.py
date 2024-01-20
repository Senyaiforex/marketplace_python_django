from typing import List, Dict, Tuple
from django.db.models import QuerySet
from productsapp.models import Product, Specific
from repositories import SpecificSelectRepository
from repositories.price_repository import PriceRepository

_price_repository = PriceRepository()
_specific_repository = SpecificSelectRepository()


class ProductSpecifics:

    """ Сервис для работы с характеристиками продукта """

    @classmethod
    def get_general_characteristics(cls, products: QuerySet[Product]) \
            -> Tuple[Dict[str, list], List[Specific]]:
        """
        Функция для получения общих характеристик и их значений.
        :param products: кверисет продуктов
        :return: tuple(dict(str, list), list)
        """
        # Список общих имен характеристик

        names = [set(product.spec_names) for product in products]
        common_names = set()
        for name_set in names:
            if common_names:
                common_names &= name_set  # пересечение множеств
            else:
                common_names |= name_set  # объединение множеств

        # Список общих характеристик

        common_spec = [
            specific
            for product in products
            for specific in product.specifics
            if specific.type_spec.name in common_names
        ]

        # Словарь, key - имя характеристики, value -
        # список разных значений данной характеристики

        spec_dict = dict()
        for spec in common_spec:
            name = spec.type_spec.name
            if name in spec_dict.keys():
                if spec.description not in spec_dict[name]:
                    spec_dict[name].append(spec.description)
            else:
                spec_dict[name] = [spec.description]

        return spec_dict, common_spec

    @classmethod
    def get_specifics(cls, products: QuerySet[Product]) -> QuerySet[Product]:
        """
        Метод для работы с спецификациями продукта.
        :param products: кверисет продуктов.
        :return: обновленный кверисет продуктов.
        """
        for product in products:
            product_price = _price_repository. \
                get_min_price_object(product=product)
            product.price = product_price.value
            # Цена
            specifics = _specific_repository.get_specific_by_product(
                product=product
            )
            # Получаем характеристики для продукта
            spec_name_list = list()
            # Список имён характеристик для данного продукта
            for specific in specifics:
                # Выделяем цветом характеристики
                current_name = specific.type_spec.name
                spec_name_list.append(current_name)

                if current_name in [
                    "Тип",
                    "Операционная система",
                    "Плотность пикселей"
                ]:
                    specific.is_comparis = True

            product.specifics = specifics
            product.spec_names = spec_name_list

        return products
