from repositories.cart_repository import RepCart, RepCartItem
from repositories.seller_select_repository import SellerSelectRepository
from repositories.product_select_repository import ProductSelectRepository
from repositories.price_repository import PriceRepository
from productsapp.models import SlicePrice
from cartapp.models import CartItem, Cart
from django.db.models import QuerySet
from typing import Union, Tuple
from .product_discounts import ProductDiscounts

rep_cart = RepCart()
rep_cart_item = RepCartItem()
rep_seller = SellerSelectRepository()
rep_prod = ProductSelectRepository()
rep_price = PriceRepository()


class SelectCart:
    """
    Сервис получения информации о корзине пользователя
    """

    @classmethod
    def cart_items_list(cls, cart: Cart = None,
                        session_products: dict = None) \
            -> Union[QuerySet[CartItem], QuerySet[SlicePrice]]:
        """
        Получение списка товаров в корзине
        Если пользователь авторизован, то методу
        передаётся экземпляр пользователя
        Если не авторизован, то передаётся словарь:
        session_products =
        {'product_id seller_id': count,...}
        """
        items_list = []
        if cart:  # пользователь авторизован
            items_list = rep_cart_item.get_all_items(cart)
            # список товаров в корзине
        else:  # есть товары в сессии
            for item in session_products:
                # цикл по ключам "product_id" и "seller_id" в сессии
                product_id, seller_id = item.split()[0], item.split()[1]
                product = rep_prod.get_product_by_id(product_id)
                seller = rep_seller.get_seller(seller_id)
                items_list.append(rep_price.get_object_price(product, seller))
        return items_list

    @classmethod
    def cart_all_products_amount(cls, cart: Cart = None,
                                 session_products: dict = None) -> int:
        """
        Получение общего количества товаров в корзине
        если есть товары в сессии, то в метод передаётся словарь
        session_products =
        {'product_id seller_id': count,...}
        """
        if cart:  # передан экземпляр пользователя(авторизован)
            count = rep_cart.count_items(cart)
        elif session_products:  # передан словарь session_products
            count = sum([count for count in
                         session_products.values()])
        else:
            count = 0
        return count

    @classmethod
    def cart_items_amount(cls, cart: Cart = None,
                          session_products: dict = None) -> int:
        """
        Получение общего количества позиций с товарами в корзине
        если есть товары в сессии, то в метод передаётся словарь
        session_products =
        {'product_id seller_id': count,...}
        """
        if cart:  # передан экземпляр пользователя(авторизован)
            count = rep_cart_item.get_count_cart_items(cart)
        elif session_products:  # передан словарь session_products
            count = len(session_products)
        else:
            count = 0
        return count

    @classmethod
    def cart_total_amount(cls, cart: Cart = None,
                          session_products: dict = None) -> float:
        """
        Получение общей цены товаров в корзине
        если есть товары в сессии, то в метод передаётся словарь
        session_products =
        {'product_id seller_id': count,...}
        """
        if cart:
            # передан экземпляр корзины пользователя(авторизован)
            total_amount = rep_cart.get_total_amount(cart)  # сумма общ
        elif session_products:  # передан словарь session_products
            cart_sum = []
            for item in session_products:
                product_id, seller_id = item.split()[0], item.split()[1]
                product = rep_prod.get_product_by_id(product_id)
                seller = rep_seller.get_seller(seller_id)
                cart_sum.append(
                    rep_price.get_price(product, seller)
                    * session_products[f'{product_id} {seller_id}'])
                #  цена на каждую позицию с товаром с учетом количества
            total_amount = sum(cart_sum)  # общая сумма корзины
        else:
            total_amount = 0
        return total_amount

    @classmethod
    def get_cart_sum_and_count(cls, cart: Cart = None,
                               session_products: dict = None) \
            -> Tuple[float, int]:
        """
        Метод возвращает кортеж из суммы корзины и количества товаров
        Для авторизованного пользователя на входе функции - cart
        Для сессий - словарь session_products
        """
        if cart:
            count = cls.cart_all_products_amount(cart=cart)
            total_sum = cls.cart_total_amount(cart=cart)
        else:
            count = cls.cart_all_products_amount(
                session_products=session_products)
            total_sum = cls.cart_total_amount(
                session_products=session_products)
        return total_sum, count

    @classmethod
    def get_dict_param_cart(cls, cart: Cart = None,
                            session_products: dict = None) -> dict:
        """
        Метод, который возвращает параметры корзины в виде словаря

        """
        if cart:
            cart_sum, cart_count = cls.get_cart_sum_and_count(
                cart=cart)
            discounted_prices_list, discount = ProductDiscounts. \
                get_prices_discount_on_cart(cart_sum, cart_count,
                                            cart=cart)
            cart_items = cls.cart_items_list(cart)
            dict_cart_param = {'cart_sum': cart_sum, 'cart_count': cart_count,
                               'cart_items': cart_items, 'discount': discount,
                               'prices_list': discounted_prices_list}
        else:
            items_list = cls.cart_items_list(
                session_products=session_products)
            cart_price = cls.cart_total_amount(
                session_products=session_products)
            count_list = [value for value in session_products.values()]
            total_count = sum(count_list)
            discounted_prices_list, discount = ProductDiscounts. \
                get_prices_discount_on_cart(cart_price, total_count,
                                            session_products=session_products)
            dict_cart_param = {'cart_sum': cart_price, 'cart_count': total_count, # noqa
                               'items_list': items_list, 'discount': discount,
                               'count_list': count_list,
                               'prices_list': discounted_prices_list}
        return dict_cart_param
