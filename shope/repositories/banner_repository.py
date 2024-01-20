from django.db.models import QuerySet
from productsapp.models import Banner
from random import sample
from django.db.models import Min
from typing import List

from interfaces.banner_interface import BannerInterface


class BannerRepository(BannerInterface):

    def get_all(self) -> QuerySet[Banner]:
        """ Метод получения всех баннеров"""
        return Banner.objects.all()

    def get_random_banners(self, quantity: int = 3) -> List[Banner]:
        """
        Метод получения случайных баннеров в определенном количестве,
        по-умолчанию - 3.
        """
        banners = Banner.objects.annotate(
            min_price=Min('category__category_products__product_price__value')
        )
        rand_banners = sample(list(banners), k=quantity)

        return rand_banners
