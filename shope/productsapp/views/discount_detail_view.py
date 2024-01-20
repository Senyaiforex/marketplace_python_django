from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views import View

from repositories import DiscountRepository, PriceRepository

_discount_repo = DiscountRepository()
_price_repository = PriceRepository()


class DiscountSetDetailView(View):
    """
    Представление для отображения
    детальной страницы скидки на набор продуктов
    """
    template_name = "productsapp/detailed_discount.html"

    def get(self, request: HttpRequest, elem_id: int) -> HttpResponse:
        set_discount = _discount_repo.get_set_discount_by_id(elem_id)
        for product in set_discount.products.all():
            product_price = _price_repository. \
                get_min_price_object(product=product).value
            product.price = product_price
        context = {
            "set_discount": set_discount,
        }
        return render(request=request,
                      template_name=self.template_name,
                      context=context)


class DiscountCartDetailView(View):
    """ Представление для отображения детальной страницы скидки на корзину """

    template_name = "productsapp/detailed_discount.html"

    def get(self, request: HttpRequest, elem_id: int) -> HttpResponse:
        cart_discount = _discount_repo.get_cart_discount_by_id(elem_id)
        context = {
            "cart_discount": cart_discount,
        }
        return render(request=request,
                      template_name=self.template_name,
                      context=context)
