from django.views.generic import View
from django.shortcuts import HttpResponseRedirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from coreapp.utils.select_cart import SelectCart
from repositories.cart_repository import RepCartItem
from repositories import RepCart
from repositories import (
    OrderUpdateRepository,
    OrderItemUpdateRepository,
    ConfigSelectRepository)

from coreapp.utils import ProductDiscounts


rep_cart = RepCart()
rep_cartitem = RepCartItem()
rep_order = OrderUpdateRepository()
rep_orderitem = OrderItemUpdateRepository()
rep_config = ConfigSelectRepository()


class AddOrderView(LoginRequiredMixin, View):
    """Класс-view для создания нового заказа"""

    def post(self, request):

        user = request.user
        cart = rep_cart.get_cart(user=user)
        count = SelectCart.cart_all_products_amount(cart=cart)
        cart_price = SelectCart.cart_total_amount(cart=cart)
        total_sum = rep_cart.get_total_amount(cart)
        discounted_sum = sum(ProductDiscounts.get_prices_discount_on_cart(
            cart_price, count, cart=cart)[0])
        sellers = rep_cartitem.sellers_amount(cart.pk)

        delivery_price = int(
            rep_config.get_config_value_by_name('DELIVERY_PRICE')
        )
        # доставка бесплатная если все товары от одного продавца и
        # сумма заказа больше требуемой
        if discounted_sum > int(
                rep_config.get_config_value_by_name('FREE_DELIVERY_SUM')
        ) and sellers == 1:
            delivery_price = 0

        order = rep_order.save(  # создание нового заказа
            user=request.user,
            delivery_price=delivery_price,
            total_price=total_sum + delivery_price,
            total_discounted_price=discounted_sum + delivery_price
        )

        # перенос позиций из корзины в заказ
        cart_items = SelectCart.cart_items_list(cart)
        rep_orderitem.create_with_cartitems(
            order=order,
            cart_items=cart_items)
        rep_cartitem.delete(cart_items)  # очистка корзины

        return HttpResponseRedirect(reverse('orderapp:edit_order',
                                            kwargs={'order_pk': order.pk}))
