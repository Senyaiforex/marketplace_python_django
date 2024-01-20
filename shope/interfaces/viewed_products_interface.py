from abc import ABC, abstractmethod
from django.db.models import QuerySet
from productsapp.models import Product
from profileapp.models import ViewedProduct
from authapp.models import User


class ViewedProductsInterface(ABC):

    @abstractmethod
    def get_all_viewed_products(self) -> QuerySet[ViewedProduct]:
        """ Get all viewed products """
        pass

    @abstractmethod
    def get_viewed_products_by_user(self,
                                    user: User,
                                    is_active: bool
                                    ) -> QuerySet[ViewedProduct]:
        """ Get all viewed products for user """
        pass

    @abstractmethod
    def get_count_viewed_for_user(self, user: User) -> QuerySet[ViewedProduct]:
        """ Get count of viewed products for user """
        pass

    @abstractmethod
    def add_product_in_viewed(self, user: User, product: Product) -> bool:
        """ Add product in viewed products"""
        pass

    @abstractmethod
    def delete_from_viewed(self, user: User, product: Product):
        """Set is_active=False for viewed product"""
        pass

    def update_viewed_product(self, product: Product, user: User):
        """update viewed product"""
        pass

    def get_viewed_product(self,
                           user: User,
                           product: Product,
                           is_active: bool = True
                           ):
        """Get product for user"""
        pass

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
        pass
