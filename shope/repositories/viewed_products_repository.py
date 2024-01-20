from django.db.models import QuerySet
from interfaces import ViewedProductsInterface
from productsapp.models import Product
from profileapp.models import ViewedProduct
from authapp.models import User
from django.utils import timezone


class ViewedProductsRepository(ViewedProductsInterface):
    """
    Repository for Viewed Products model
    """
    def delete_from_viewed(self, product: Product, user: User):
        viewed = ViewedProduct.objects.get(
            product=product,
            user=user,
            is_active=True
        )
        viewed.is_active = False
        viewed.save()

    def add_product_in_viewed(
            self,
            user: User,
            product: Product
    ) -> ViewedProduct:
        viewed_product = ViewedProduct(
            user=user,
            product=product
        )
        viewed_product.save()
        return viewed_product

    def get_count_viewed_for_user(self, user: User) -> int:
        """ Get count of viewed products for user"""
        return ViewedProduct.objects.filter(
            user=user,
            is_active=True
        ).count()

    def get_all_viewed_products(self) -> QuerySet[ViewedProduct]:
        """ Get all viewed products """
        return ViewedProduct.objects.all()

    def get_viewed_products_by_user(
            self,
            user: User,
            is_active: bool = True
    ) -> QuerySet[ViewedProduct]:

        """ Get all viewed products for user """
        return ViewedProduct.objects.filter(
            user=user,
            is_active=is_active
        ).order_by('-updated_at')

    def get_viewed_product(
            self,
            user: User,
            product: Product,
            is_active: bool = True
    ):
        return ViewedProduct.objects.filter(
            user=user,
            product=product,
            is_active=is_active
        )

    def update_viewed_product(self, product: Product, user: User):
        """update update_at viewed product"""

        viewed_product = ViewedProduct.objects.filter(
                user=user,
                product=product,
                is_active=True
            )

        viewed_product.update(updated_at=timezone.now())
        return viewed_product

    def get_by_user_limit(
            self,
            user: User,
            limit: int,
            is_active: bool = True
    ) -> QuerySet[ViewedProduct]:

        """
        Получить просмотренные продукты для пользователя
        с ограничением на количество
        """
        return ViewedProduct.objects.filter(
            user=user,
            is_active=is_active
        ).order_by('-updated_at')[:limit]
