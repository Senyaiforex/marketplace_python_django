from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from coreapp.utils.products_comparison_list import ProductsComparisonList
from coreapp.utils.working_with_product_characteristics import ProductSpecifics
from repositories import SpecificSelectRepository
from repositories.price_repository import PriceRepository

_price_repository = PriceRepository()
_specific_repository = SpecificSelectRepository()


class ProductComparisonView(View):
    """
    Класс-view для сравнения товаров
    """
    template_name = "productsapp/comparison.html"
    _service = ProductsComparisonList()
    _product_specifics_service = ProductSpecifics()

    def get(self, request: HttpRequest) -> HttpResponse:
        products = self._service.get_comparison_list(request) or []
        for product in products:
            product_price = _price_repository. \
                get_min_price_object(product=product)
            product.price = product_price.value
            specifics = _specific_repository.get_specific_by_product(
                product=product
            )
            for specific in specifics:
                if specific.type_spec.name in [
                    "Тип",
                    "Операционная система",
                    "Плотность пикселей"
                ]:
                    specific.is_comparis = True
            product.specifics = specifics

        # Множество общих категорий, если разные
        # категории у разных продуктов - не сравниваем
        common_category: set = {product.category for product in products}

        return render(request=request,
                      template_name=self.template_name,
                      context={
                          "products": products,
                          "number_of_products":
                              self._service.comparison_list_size(request),
                          "is_common_spec": True
                          if len(common_category) > 1
                          else False,
                      })

    def post(self, request: HttpRequest):
        products = self._service.get_comparison_list(request) or []
        products = self._product_specifics_service.get_specifics(products)
        spec_dict, common_spec = self._product_specifics_service.\
            get_general_characteristics(products)

        if "is_different" in request.POST:
            # Только различающиеся характеристики
            for product in products:
                new_specifics = list()
                # Обновленный список характеристик
                for specific in product.specifics:
                    name = specific.type_spec.name
                    if name in spec_dict.keys() \
                            and specific.description in spec_dict[name] \
                            and len(spec_dict[name]) > 1:
                        new_specifics.append(specific)
                        # Отсеиваем характеристики, которых нет в общем списке
                        # и у которых одинаковые характеристики
                product.specifics = new_specifics

        common_category: set = {product.category for product in products}

        return render(request=request,
                      template_name=self.template_name,
                      context={
                          "products": products,
                          "number_of_products":
                              self._service.comparison_list_size(request),
                          "is_common_spec": True
                          if not common_spec or len(common_category) > 1
                          else False,
                      })
