from abc import ABC, abstractmethod
from productsapp.models import Product


class PriceInterface(ABC):

    @abstractmethod
    def get_avg_prices(self, product: Product) -> int:
        """
        Получить среднее значение цен конкретного продукта

        :param product: продукт, у которого нужно узнать цену

        :return: усредненная цена
        """
        pass
