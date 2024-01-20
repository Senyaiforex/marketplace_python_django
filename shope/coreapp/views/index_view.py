from django.views.generic import View
from django.shortcuts import render
from django.conf import settings
from repositories import (
    SliderRepository,
    BannerRepository,
    ProductSelectRepository,
    DiscountRepository
)

slider_rep = SliderRepository()
banner_rep = BannerRepository()
product_rep = ProductSelectRepository()
discount_rep = DiscountRepository()


class IndexView(View):

    template_name = 'index.html'

    def get(self, request):

        sliders = slider_rep.get_all()
        banners = banner_rep.get_random_banners()

        products = product_rep.get_all_products_with_main_image()

        products_with_price = product_rep.get_product_prices(products)

        discount_product = discount_rep.get_product_with_discount()
        discount_product = product_rep.get_product_prices(discount_product)

        popular = product_rep.sort_by_popular(
            products=products_with_price,
            reverse=True
        )[:settings.MAX_POPULAR_INDEX]

        limited = products_with_price.filter(is_limited=True)

        context = {
            'sliders': sliders,
            'banners': banners,
            'populars': popular,
            'limited': limited,
            'discounted': discount_product.first()
        }

        return render(request, self.template_name, context=context)
