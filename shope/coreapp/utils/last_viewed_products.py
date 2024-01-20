from authapp.models import User
from productsapp.models import Product
from repositories import ViewedProductsRepository, ConfigSelectRepository

viewed_products_rep = ViewedProductsRepository()
config_rep = ConfigSelectRepository()


class ViewedProductsService:
    """
    Сервис для работы с просмотренными товарами
    """
    def _delete_last_for_user(self, user: User):
        """
        Удаление просмотренного продукта не входящего в лимит по просмотренным
        """
        products = viewed_products_rep.get_viewed_products_by_user(user=user)
        last_product = products.order_by('updated_at').last()
        print(last_product)
        viewed_products_rep.delete_from_viewed(
            product=last_product.product,
            user=last_product.user
        )

    def add_to_viewed_products(self, user: User, product: Product):
        """
        Добавить товар к списку просмотренных товаров
        """
        viewed_count = viewed_products_rep.get_count_viewed_for_user(user=user)

        if viewed_products_rep.get_viewed_product(
            user=user,
            product=product
        ):

            viewed_product = viewed_products_rep.update_viewed_product(
                product=product,
                user=user
            )
            return viewed_product

        if viewed_count >= config_rep.get_config_value_by_name(
                'MAX_VIEWED_PRODUCTS'
        ):
            self._delete_last_for_user(user=user)
            viewed_product = viewed_products_rep.add_product_in_viewed(
                user=user,
                product=product
            )
            return viewed_product

        viewed_products_rep.add_product_in_viewed(user=user, product=product)
