from cartapp.models import CartItem, Cart
from authapp.models import User
from django.db.models import F

from repositories.cart_repository import RepCart, RepCartItem
from repositories.seller_select_repository import SellerSelectRepository
from repositories.product_select_repository import ProductSelectRepository
from repositories.price_repository import PriceRepository
from typing import Union, NoReturn

rep_cart = RepCart()
rep_cart_item = RepCartItem()
rep_seller = SellerSelectRepository()
rep_prod = ProductSelectRepository()
rep_price = PriceRepository()


class AddToCart:
    """
    Сервис добавления товара в корзину,
    удаления его из корзины и изменения
    количества товара в корзине
    """

    @classmethod
    def add_to_cart(cls, product_id: int, seller_id: int, count: int = 1,
                    cart: Cart = None, session_products: dict = None) \
            -> Union[NoReturn, dict]:
        """
        Метод добавления товара в корзину
        Если есть словарь с товарами из сессии <session_products>,
        то метод вернёт обновлённый словарь для обновления текущей сессии.
        """
        if cart:  # если пользователь авторизован
            product = rep_prod.get_product_by_id(product_id)
            seller = rep_seller.get_seller(seller_id)
            cart_item = rep_cart_item.get_cart_item(
                cart=cart, product=product, seller=seller)
            if not cart_item:  # товара нет в корзине
                rep_cart_item.save(cart=cart, product=product,
                                   seller=seller, quantity=count)
            else:  # товар есть в корзине
                cart_item.update(quantity=F('quantity') + count)
        else:  # анонимный пользователь
            key = f'{product_id} {seller_id}'
            if session_products:  # если есть товары в сессии
                if session_products.get(key):
                    session_products[key] += count
                else:  # позиция с товаром отсутствует
                    session_products[key] = count
            else:  # в сессии нет товаров
                session_products = {key: count}
            return session_products

    @classmethod
    def delete_from_cart(cls, product_id: int, seller_id: int, count: int = 1,
                         cart: Cart = None, session_products: dict = None,
                         full=None) -> Union[NoReturn, dict]:
        """
        Удаление товара из корзины
        Если есть словарь с товарами из сессии <session_products>,
        то метод вернёт обновлённый словарь для обновления текущей сессии.
        """
        if cart:  # если пользователь авторизован
            product = rep_prod.get_product_by_id(product_id)
            seller = rep_seller.get_seller(seller_id)
            cart_item = rep_cart_item. \
                get_cart_item(cart=cart, product=product, seller=seller)
            if full or cart_item.first().quantity == 1:
                rep_cart_item.delete(cart_item)  # удаление всей позиции
            else:  # уменьшение количества товара на count
                cart_item.update(quantity=F('quantity') - count)
        else:
            key = f'{product_id} {seller_id}'
            if session_products:  # если есть товары в сессии
                if full or session_products[key] == 1:
                    # удаление товара из корзины
                    session_products.pop(key, False)
                else:  # уменьшение количества на 1
                    session_products[key] -= count
                return session_products

    @classmethod
    def change_amount(cls, product_id: int, seller_id: int,
                      count: int, cart: Cart = None,
                      session_products: dict = None) \
            -> Union[NoReturn, dict]:
        """
        Изменить количество товара в корзине
        Если есть словарь с товарами из сессии <session_products>,
        то метод вернёт обновлённый словарь для обновления текущей сессии.
        """
        if cart:
            product = rep_prod.get_product_by_id(product_id)
            seller = rep_seller.get_seller(seller_id)
            cart_item = CartItem.objects.get(cart=cart,
                                             product=product,
                                             seller=seller)
            #  позиция с товаром в корзине
            rep_cart_item.save(force=cart_item, quantity=count)
            # изменение количества товара в корзине
        else:
            if session_products:  # если есть товары в сессии
                session_products[f'{product_id} {seller_id}'] = count
                # изменение количества товара в корзине
                return session_products

    @classmethod
    def move_from_session(cls, user: User, session_products: dict)\
            -> NoReturn:
        """
        Добавление товаров в корзину пользователя
        из сессии
        """
        cart = rep_cart.get_cart(user)
        if session_products:
            for item in session_products:
                # цикл по ключам в сессии
                product_id, seller_id = item.split()[0], item.split()[1]
                product = rep_prod.get_product_by_id(product_id)
                seller = rep_seller.get_seller(int(seller_id))
                cart_item = rep_cart_item. \
                    get_cart_item(cart=cart, product=product, seller=seller)
                key = f'{product_id} {seller_id}'
                if cart_item:  # позиция с этим товаром в корзине уже есть
                    count = session_products[key]
                    cart_item.update(quantity=F('quantity') + count)
                else:
                    rep_cart_item.save(
                        cart=cart, product=product,
                        seller=seller, quantity=session_products[key]
                    )
                # создание позиций в корзине
