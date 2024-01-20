from repositories import ProductSelectRepository, DiscountRepository, \
    PriceRepository, SellerSelectRepository
from repositories.cart_repository import RepCartItem
from typing import List
from cartapp.models import CartItem, Cart
from productsapp.models import Product, Category, CartDiscount, \
    SetDiscount, ProductDiscount
from typing import Union, NoReturn, Tuple
from datetime import datetime
from django.db.models import Value, QuerySet

product_repository = ProductSelectRepository()
discount_rep = DiscountRepository()
cartitem_rep = RepCartItem()
rep_price = PriceRepository()
rep_prod = ProductSelectRepository()
rep_seller = SellerSelectRepository()


class ProductDiscounts:
    """
    Сервис получения скидок на товары
    """

    @classmethod
    def get_objects_discounts_list(
            cls, discount_queryset: QuerySet[ProductDiscount]) \
            -> Tuple[List[Product], List[Category]]:
        """
        Метод, который возвращает список всех товаров
        и категорий со скидкой с аннотацией по датам
        действия скидки
        """
        products = [discount.products.filter(is_active=True).annotate(
            value=Value(discount.value), type=Value('product'),
            start_date=Value(datetime.strftime(discount.start_date,
                                               '%b-%d-%Y')),
            expiration_date=Value(
                datetime.strftime(discount.expiration_date, '%b-%d-%Y')) if
            discount.expiration_date else Value('')
        ) for discount in
            discount_queryset]  # все товары, у которых есть скидка
        categories = [discount.categories.filter(is_active=True).annotate(
            value=Value(discount.value), type=Value('category'),
            start_date=Value(datetime.strftime(discount.start_date,
                                               '%b-%d-%Y')),
            expiration_date=Value(
                datetime.strftime(discount.expiration_date, '%b-%d-%Y')) if
            discount.expiration_date else Value('')
        ) for discount in
            discount_queryset]  # все категории со скидками
        return products, categories

    @classmethod
    def get_priority_product_discount(cls, product: Product,
                                      category: Category) -> float:
        """
        Метод возвращает приоритетную скидку на товар или категорию
        """
        discount = discount_rep. \
            get_discount_by_product_or_category(product=product,
                                                category=category)
        return discount

    @classmethod
    def get_priority_cart_discount(cls, cart_price: float, count: int) \
            -> Union[int, CartDiscount]:
        """
        Получение приоритетной скидки на корзину.
        Возвращает экземпляр CartDiscount, если есть скидка на
        корзину и необходимые условия для скидки выполнены
        """
        discount = discount_rep.get_discount_by_cart()
        discount_conditions = False
        if not discount:
            return False
        if discount.required_sum and discount.required_quantity:
            if cart_price >= discount.required_sum \
                    and count >= discount.required_quantity:
                # условия выполнены
                discount_conditions = discount
        elif discount.required_sum \
                and not discount.required_quantity:
            # условие одно - сумма корзины
            if cart_price >= discount.required_sum:
                discount_conditions = discount
        elif discount.required_quantity \
                and not discount.required_sum:
            # условие одно - количество товаров
            if count >= discount.required_quantity:
                discount_conditions = discount
        return discount_conditions

    @classmethod
    def get_priority_set_discount(cls, products_id: List[int]) \
            -> Union[NoReturn, SetDiscount]:
        """
        Проверить корзину на наличие скидочных наборов
        и вернуть скидку на приоритетный набор
        """
        # множество товаров, содержащихся в позициях корзины
        cart_prod_set = set(
            product_repository.get_products_with_these_id(products_id))

        result_discounts = list()

        for product in cart_prod_set:
            # все скидочные наборы, где есть данный продукт
            current_discounts = discount_rep.get_set_discounts_for_product(
                product=product)

            # проверка вхождения множества товаров из набора
            # в множество товаров корзины
            for discount in current_discounts:
                disc_prod_set = set(
                    product_repository.get_products_from_set(discount))
                if disc_prod_set.issubset(cart_prod_set):
                    result_discounts.append(discount)
        if result_discounts:
            priority_discount = max(result_discounts,
                                    key=lambda discount: discount.priority)
        else:
            return None
        return priority_discount

    @classmethod
    def apply_products_discount(cls, cart: Cart = None,
                                session_products: dict = None) \
            -> List[float]:
        """
        Метод применяет скидку к каждому товару
        Если пользователь авторизован, то в метод передаётся
        экземпляр корзины пользователя - cart, если нет, то словарь
        session_products =
        {'product_id seller_id': count,...}
        Метод возвращает список цен на товары в корзине с учетом скидки
        """
        if cart:
            result_prices = ApplyDiscount.\
                apply_discount_products_for_cart(cart)
        else:
            result_prices = ApplyDiscount.\
                apply_discount_products_for_session(session_products)
        return result_prices

    @classmethod
    def apply_set_discount(cls, set_discount: SetDiscount, cart: Cart = None,
                           session_products: dict = None) \
            -> List[float]:
        """
        Метод применяет скидку к набору товаров
        Если пользователь авторизован, то в метод передаётся
        экземпляр корзины пользователя - cart, если нет, то словарь
        session_products =
        {'product_id seller_id': count,...}
        Метод возвращает список цен на каждый товар
        в корзине со скидкой
        """
        if cart:
            result_prices = ApplyDiscount.\
                apply_set_discounts_for_cart(cart, set_discount)
        else:
            result_prices = ApplyDiscount.\
                apply_set_discounts_for_session(session_products, set_discount)
        return result_prices

    @classmethod
    def apply_cart_discount(cls, cart_discount: CartDiscount,
                            cart_price: float,
                            cart: Cart = None,
                            session_products: dict = None) -> List[float]:
        """
        Метод применяет скидку на корзину
        и возвращает список цен на товары в корзине
        """

        if cart:  # пользователь авторизован
            result_prices = ApplyDiscount.\
                apply_cart_discount_for_user(cart, cart_discount)
        else:
            result_prices = ApplyDiscount.\
                apply_cart_discount_for_session(session_products,
                                                cart_discount)
        return result_prices

    @classmethod
    def get_prices_discount_on_cart(cls, cart_price: float, count: int,
                                    cart: Cart = None,
                                    session_products: dict = None) \
            -> Tuple[List[float], Union[CartDiscount, SetDiscount]]:
        """
        В методе происходит определение наиболее приоритетной схемы скидки
        Если пользователь авторизован, то в метод передаётся
        экземпляр корзины пользователя - cart, если нет, то словарь
        session_products =
        {'product_id seller_id': count,...}
        Метод возвращает список цен на товары в корзине,
        и тип применённой скидки
        """
        discount = None
        if cart:  # пользователь авторизован
            products_id = product_repository.get_products_id_from_cart(cart)
            cart_discount = cls. \
                get_priority_cart_discount(cart_price, count)
            set_discount = cls. \
                get_priority_set_discount(products_id)
            if cart_discount and set_discount:  # обе скидки
                if cart_discount.priority >= set_discount.priority:
                    cart_prices_list = cls. \
                        apply_cart_discount(cart_discount, cart_price,
                                            cart=cart)
                    discount = cart_discount
                else:
                    cart_prices_list = cls. \
                        apply_set_discount(set_discount, cart=cart)
                    discount = set_discount
            elif cart_discount:  # только скидка на корзину
                cart_prices_list = cls. \
                    apply_cart_discount(cart_discount, cart_price,
                                        cart=cart)
                discount = cart_discount
            elif set_discount:  # только скидка на набор
                cart_prices_list = cls. \
                    apply_set_discount(set_discount, cart=cart)
                discount = set_discount
            else:  # подсчет скидки на каждый товар, если есть
                cart_prices_list = cls. \
                    apply_products_discount(cart)
                discount = cart_discount
        elif session_products:  # товары есть в сессии
            products_id = [item.split()[0] for item in session_products.keys()]
            cart_discount = cls. \
                get_priority_cart_discount(cart_price, count)
            set_discount = cls. \
                get_priority_set_discount(products_id)
            if cart_discount and set_discount:
                if cart_discount.priority >= set_discount.priority:
                    cart_prices_list = cls. \
                        apply_cart_discount(cart_discount,
                                            cart_price,
                                            session_products=session_products)
                    discount = cart_discount
                else:
                    cart_prices_list = cls. \
                        apply_set_discount(set_discount,
                                           session_products=session_products)
                    discount = set_discount
            elif cart_discount:
                cart_prices_list = cls. \
                    apply_cart_discount(cart_discount,
                                        cart_price,
                                        session_products=session_products)
                discount = cart_discount
            elif set_discount:
                cart_prices_list = cls. \
                    apply_set_discount(set_discount,
                                       session_products=session_products)
                discount = set_discount
            else:
                cart_prices_list = cls. \
                    apply_products_discount(session_products=session_products)
        else:
            cart_prices_list = []
        return cart_prices_list, discount


class ApplyDiscount:
    """
    Класс для применения скидок к товарам
    """

    @classmethod
    def apply_discount_products_for_cart(cls, cart: Cart) -> List[float]:
        """
        Для авторизованного пользователя.
        Метод применения скидки к каждому товару в корзине,
        возвращает список цен на товары в корзине с учётом скидки
        """
        cart_prices = []
        items = cartitem_rep.get_all_items(cart)
        for item in items:  # цикл по каждой позиции с товаром
            category = item.product.category
            discount = ProductDiscounts. \
                get_priority_product_discount(item.product, category)
            price = item.price
            if discount:  # есть скидка, цена считается со скидкой
                discounted_price = (price - price * discount.value / 100)
                price = discounted_price * item.quantity
            else:  # цена без скидки
                price = item.price * item.quantity
            item.discounted_price = round(float(price), 2)
            cart_prices.append(item.discounted_price)
        CartItem.objects.bulk_update(items,
                                     ['discounted_price'], batch_size=20)
        return cart_prices

    @classmethod
    def apply_discount_products_for_session(cls, session_products: dict) \
            -> List[float]:
        """
        Для товаров, хранящихся в сессии.
        Метод применения скидки к каждому товару в сессии,
        принимает словарь session_products =
        {'product_id seller_id': count,...}
        возвращает список цен на товары в корзине с учётом скидки
        """
        cart_prices = []
        for item in session_products:
            # цикл по товарам в словаре session_products
            product = rep_prod.get_product_by_id(item.split()[0])
            seller = rep_seller.get_seller(item.split()[1])
            price = rep_price.get_price(product=product,
                                        seller=seller)
            discount = ProductDiscounts. \
                get_priority_product_discount(product, product.category)
            if discount:  # если скидка, рассчитывается цена со скидкой
                price = (price - price * discount.value / 100) \
                        * session_products[item]
            else:  # цена без скидки
                price = price * session_products[item]
            cart_prices.append(round(float(price), 2))
        return cart_prices

    @classmethod
    def apply_set_discounts_for_cart(cls, cart: Cart,
                                     set_discount: SetDiscount) \
            -> List[float]:
        """
        Для авторизованного пользователя.
        Метод для применения скидки на набор товаров.
        Возвращает список цен в корзине с учетом скидки
        """
        products_discounted = set_discount.products.all()
        cart_prices = []
        items = cartitem_rep.get_all_items(cart)
        for item in items:
            price = item.price
            if item.product in products_discounted:
                # товар есть в наборе
                discounted_price = (price - price *
                                    set_discount.value / 100)
                price = discounted_price * item.quantity
            else:  # цена без скидки
                price = item.price * item.quantity
            item.discounted_price = round(float(price), 2)
            cart_prices.append(item.discounted_price)
        CartItem.objects.bulk_update(
            items, ['discounted_price'], batch_size=20
        )
        return cart_prices

    @classmethod
    def apply_set_discounts_for_session(cls, session_products: dict,
                                        set_discount: SetDiscount) \
            -> List[float]:
        """
        Для товаров, хранящихся в сессии.
        Метод для применения скидки на набор товаров.
        Возвращает список цен в корзине с учетом скидки
        """
        products_discounted = set_discount.products.all()
        cart_prices = []
        for item in session_products:
            product = rep_prod.get_product_by_id(item.split()[0])
            seller = rep_seller.get_seller(item.split()[1])
            price = rep_price.get_price(product=product,
                                        seller=seller)
            if product in products_discounted:
                # товар в наборе
                price = float((price - price *
                               set_discount.value / 100) *
                              session_products[item])
            else:  # у товара нет скидки
                price = float(price * session_products[item])
            cart_prices.append(round(price, 2))
        return cart_prices

    @classmethod
    def apply_cart_discount_for_user(cls, cart: Cart,
                                     cart_discount: CartDiscount) \
            -> List[float]:
        """
        Для авторизованного пользователя.
        Метод применяет скидку на корзину
        и возвращает список цен на товары в корзине
        """
        discount = cart_discount.value
        cart_prices = []
        items = cartitem_rep.get_all_items(cart)
        for item in items:
            price = item.price
            discounted_price = (price - price * discount / 100)
            price = round(float(discounted_price * item.quantity), 2)
            item.discounted_price = price
            cart_prices.append(price)
        CartItem.objects.bulk_update(
            items, ['discounted_price'], batch_size=20
        )
        return cart_prices

    @classmethod
    def apply_cart_discount_for_session(cls, session_products: dict,
                                        cart_discount: CartDiscount) \
            -> List[float]:
        """
        Для товаров, хранящихся в сессии.
        Метод применяет скидку на корзину
        и возвращает список цен на товары в корзине
        """
        discount = cart_discount.value
        cart_prices = []
        for item in session_products:
            product = rep_prod.get_product_by_id(item.split()[0])
            seller = rep_seller.get_seller(item.split()[1])
            price = rep_price.get_price(product=product,
                                        seller=seller)
            price = float((price - price * discount / 100) *
                          session_products[item])
            cart_prices.append(round(price, 2))
        return cart_prices
