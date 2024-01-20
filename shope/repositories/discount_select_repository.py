from interfaces.discount_select_interface import DiscountInterface
from datetime import datetime
from productsapp.models import CartDiscount, SetDiscount, \
    Product, Category, ProductDiscount
from django.db.models import QuerySet, Q, Value


class DiscountRepository(DiscountInterface):
    """
    Репозиторий для работы со скидками
    """

    def get_discount_by_product_or_category(self, product: Product,
                                            category: Category) -> float:
        """
        Метод получения скидки на товар и/или категорию
        возвращает значение скидки
        """
        date_now = datetime.now()
        product_discount = product.product_discounts.filter(
            start_date__lte=date_now, expiration_date__gte=date_now,
            is_active=True).order_by('-priority').only('value', 'priority')[:1]
        # наиболее приоритетная скидка на товар, если есть
        category_discount = category.category_discounts.filter(
            start_date__lte=date_now, expiration_date__gte=date_now,
            is_active=True).order_by('-priority').only('value', 'priority')[:1]
        # наиболее приоритетная скидка на категорию, если есть
        total = (category_discount | product_discount). \
            order_by('-priority').first()
        # наиболее приоритетная скидка среди категорий и товаров
        if total:
            return total
        else:
            return False

    def get_discount_by_cart(self) -> CartDiscount:
        """
        Метод получения скидки на корзину
        возвращает экземпляр CartDiscount
        """
        date_now = datetime.now()
        cart_discount = CartDiscount.objects.filter(
            start_date__lte=date_now, expiration_date__gte=date_now,
            is_active=True).order_by('-priority') \
            .only('required_sum', 'required_quantity',
                  'value', 'priority').first()
        return cart_discount

    def get_set_discounts_for_product(
            self, product: Product) -> QuerySet[SetDiscount]:
        """
        Получить все скидки на наборы, в которых есть данный продукт
        """
        date_now = datetime.now()
        return product.set_discounts.filter(start_date__lte=date_now,
                                            expiration_date__gte=date_now,
                                            is_active=True)

    def get_set_discounts_all(self):
        """
        Получить все скидки на наборы, которые
        действуют сейчас или будут действовать
        в будущем
        """
        date_now = datetime.now()
        set_discounts = SetDiscount.objects.filter(
            Q(expiration_date__gte=date_now) |
            Q(expiration_date__isnull=True), is_active=True) \
            .annotate(type=Value('set')) \
            .order_by('-start_date')
        return set_discounts

    def get_cart_discounts_all(self):
        """
        Получить все скидки на корзину, которые
        действуют сейчас или будут действовать
        в будущем
        """
        date_now = datetime.now()
        cart_discounts = CartDiscount.objects.filter(
            Q(expiration_date__gte=date_now) |
            Q(expiration_date__isnull=True), is_active=True) \
            .annotate(type=Value('cart')) \
            .order_by('-start_date')
        return cart_discounts

    def get_products_discounts_all(self):
        """
        Получить все скидки на товары, которые
        действуют сейчас или будут действовать
        в будущем
        """
        date_now = datetime.now()
        products_discounts = ProductDiscount.objects.filter(
            Q(expiration_date__gte=date_now) |
            Q(expiration_date__isnull=True), is_active=True) \
            .order_by('-start_date') \
            .prefetch_related('products', 'categories')
        return products_discounts

    def get_product_with_discount(self):
        """
        Получить товары с активными скидками
        """
        date_now = datetime.now()

        products = Product.objects.filter(
            product_discounts__start_date__lte=date_now,
            product_discounts__expiration_date__gte=date_now,
            product_discounts__is_active=True
        ).order_by('updated_at').prefetch_related('product_discounts')
        return products

    def get_set_discount_by_id(self, set_id: int) -> SetDiscount:
        return SetDiscount.objects.get(id=set_id)

    def get_cart_discount_by_id(self, cart_id: int) -> CartDiscount:
        return CartDiscount.objects.get(id=cart_id)
