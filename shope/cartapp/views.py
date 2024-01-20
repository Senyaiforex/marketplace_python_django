from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from coreapp.utils import AddToCart, SelectCart, ProductDiscounts
from repositories import DiscountRepository, RepCart
from .forms import InputAmountForm
from django.http import HttpResponse

disc_rep = DiscountRepository()
cart_rep = RepCart()


class CartItemListView(View):
    """
    Класс для отображения всех товаров в корзине
    """
    template_name = 'cartapp/cart.html'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated:  # пользователь авторизован
            cart = cart_rep.get_cart(user=request.user)
            cart_items = SelectCart.cart_items_list(cart)
            context = {'items': cart_items, 'session': False}
            return render(request, self.template_name, context=context)
        else:  # пользователь не авторизован
            if request.session.get('products', False):  # есть товары в сессии
                items_price = SelectCart. \
                    cart_items_list(session_products=request.session['products']) # noqa
                count_list = [val for val in request.session['products'].values()] # noqa
                session_products = request.session.get('products')
                cart_price, count = SelectCart.get_cart_sum_and_count(
                    session_products=session_products)
                discounted_prices_list, discount = ProductDiscounts. \
                    get_prices_discount_on_cart(
                        cart_price, count, session_products=session_products)
                request.session['prices'] = discounted_prices_list
                request.session.modified = True
                context = {'items': zip(count_list, items_price,
                                        discounted_prices_list),
                           'session': True, 'count_cart': count,
                           'total_amount': round(sum(discounted_prices_list),
                                                 2),
                           'discount': discount}
                return render(request, self.template_name, context)
            else:
                return render(request, self.template_name)


class AjaxUpdateCartView(View):
    method_service = AddToCart.add_to_cart
    full_delete = False  # флаг для удаления всей позиции с товаром

    def post(self, request, **kwargs) -> JsonResponse:
        form = InputAmountForm(request.POST)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if form.is_valid():  # передано валидное значение count
                cleaned_data = {key: val for key, val in
                                form.cleaned_data.items() if val is not None}
                if self.full_delete:
                    cleaned_data['full'] = True
                if request.user.is_authenticated:  # пользователь авторизован
                    cart = cart_rep.get_cart(user=request.user)  # корзина
                    self.method_service(**cleaned_data, cart=cart)
                    dict_params = SelectCart.get_dict_param_cart(cart)
                    cart_items_html = render_to_string(
                        'cartapp/cart_ajax.html',
                        context={'items': dict_params['cart_items'],
                                 'cart_sum': round(sum(dict_params['prices_list']), 2),  # noqa
                                 'discount': dict_params['discount'],
                                 })
                    context = {'cart_count': dict_params['cart_count'],
                               'items': cart_items_html,
                               'cart_sum': round(sum(dict_params['prices_list']), 2) # noqa
                               }
                    return JsonResponse(data=context, safe=False)
                else:
                    session_products = request.session.get('products')
                    products = self. \
                        method_service(**cleaned_data, session_products=session_products)  # noqa
                    request.session['products'] = products
                    dict_params = SelectCart.get_dict_param_cart(session_products=products)  # noqa
                    request.session['prices'] = dict_params['prices_list']
                    request.session.modified = True
                    cart_items_html = render_to_string(
                        'cartapp/cart_ajax.html',
                        context={
                            'items': list(zip(
                                dict_params['count_list'],
                                dict_params['items_list'],
                                dict_params['prices_list']
                            )),
                            'session': True, 'discount': dict_params['discount'], # noqa
                            'cart_sum': round(sum(dict_params['prices_list']), 2) # noqa
                        })
                    context = {'items': cart_items_html,
                               'cart_count': dict_params['cart_count'],
                               'cart_sum': round(sum(dict_params['prices_list']), 2) # noqa
                               }
                    return JsonResponse(data=context, safe=False)


class AddToCartAjaxView(AjaxUpdateCartView):
    method_service = AddToCart.add_to_cart


class ReduceFromCartAjaxView(AjaxUpdateCartView):
    method_service = AddToCart.delete_from_cart


class DeleteCartItemAjaxView(AjaxUpdateCartView):
    method_service = AddToCart.delete_from_cart
    full_delete = True


class ChangeQuantityCartAjaxView(AjaxUpdateCartView):
    """
    Класс для изменения количества товара в корзине
    """
    method_service = AddToCart.change_amount
