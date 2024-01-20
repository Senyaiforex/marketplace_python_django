from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from coreapp.utils.products_comparison_list import ProductsComparisonList
from repositories import SpecificSelectRepository
from repositories.price_repository import PriceRepository


_price_repository = PriceRepository()
_specific_repository = SpecificSelectRepository()


class RemoveFromComparisonView(View):
    """
    Класс-view для сравнения товаров
    """
    template_name = "productsapp/comparison.html"
    _service = ProductsComparisonList()

    def post(self, request: HttpRequest, product_id: int):
        self._service.remove_from_comparison(request, product_id)
        return HttpResponseRedirect(reverse("productsapp:comparison"))
