from itertools import chain
from django.views.generic import View
from django.shortcuts import render
from repositories.discount_select_repository import DiscountRepository
from django.core.paginator import Paginator
from django.http import HttpResponse
from coreapp.utils import ProductDiscounts
rep_discount = DiscountRepository()


class DiscountsListView(View):
    """
    Класс для отображения всех скидок
    """
    template_name = 'productsapp/sale.html'
    paginate_by = 12

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """
        Метод для отображения всех имеющихся скидок
        """
        set_discounts = rep_discount.get_set_discounts_all()
        cart_discounts = rep_discount.get_cart_discounts_all()
        products_discounts = rep_discount.get_products_discounts_all()
        products, categories = ProductDiscounts.\
            get_objects_discounts_list(products_discounts)
        result_list = list(chain(cart_discounts, set_discounts,
                                 *categories, *products))
        # общий список всех скидок на товары, корзины, наборы товаров
        paginator = Paginator(result_list, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj}
        return render(request, self.template_name, context)
