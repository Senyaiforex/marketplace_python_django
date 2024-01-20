from django.db.models import QuerySet

from interfaces.sellers_select_interface import SellerSelectInterface
from productsapp.models import Product, Seller


from django.shortcuts import get_object_or_404


class SellerSelectRepository(SellerSelectInterface):
    """
    Репозиторий для модели продавцов
    """
    def get_seller(self, seller_id: int) -> Seller:
        """
        Получение объекта продавца по id
        """
        seller = get_object_or_404(Seller, pk=seller_id)
        return seller

    def get_seller_by_product(self, product: Product) -> QuerySet[Seller]:
        sellers = Seller.objects.filter(
            seller_items__product=product
        )
        return sellers

    def get_all_sellers(self) -> QuerySet[Seller]:
        pass

    def get_sellers_count(self) -> int:
        return Seller.objects.count()
