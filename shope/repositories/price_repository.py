from django.db.models import Avg, Min
from interfaces.price_interface import PriceInterface
from productsapp.models import Product, SlicePrice, Seller


class PriceRepository(PriceInterface):
    """
    Репозиторий для работы с ценами на товары
    """

    def get_avg_prices(self, product: Product) -> int:
        average_price = SlicePrice.objects.filter(
            product=product
        ).aggregate(
            price=Avg("value")
        )
        return average_price.get("price")

    def get_min_price_object(self, product: Product) -> SlicePrice:
        """
        Возвращает SlicePrice продукта, у которого минимальная цена
        """
        min_price = SlicePrice.objects. \
            filter(product=product, is_active=True). \
            annotate(min_value=Min('value')). \
            latest('-min_value', 'updated_at')
        return min_price

    def get_price(self, product: Product, seller: Seller) -> float:
        """
        Метод возвращает последнее значение цены на продукт,
        установленную продавцом.
        """
        price = SlicePrice.objects.order_by('-updated_at'). \
            filter(seller=seller, product=product,
                   is_active=True). \
            values('value').first()
        return price['value']

    def get_object_price(self, product: Product, seller: Seller) -> SlicePrice:
        """
        Метод возвращает объект SlicePrice
        """
        price_object = SlicePrice.objects. \
            select_related('seller', 'product'). \
            order_by('-updated_at'). \
            filter(product=product, seller=seller,
                   is_active=True).first()
        return price_object
