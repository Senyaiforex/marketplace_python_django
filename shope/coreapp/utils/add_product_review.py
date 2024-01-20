from productsapp.models import Product, Review
from profileapp.models import Profile
from repositories.reviews_repository import ReviewRepository


_repository = ReviewRepository()


class AddProductReview:
    """
    Сервис добавления отзыва к товару
    """

    @staticmethod
    def add_product_review(user: Profile,
                           product: Product,
                           text: str):
        """
        Добавление отзыва к товару

        :param user: объект User, который дает отзыв
        :param product: объект Product, которому адресован отзыв
        :param text: текст отзыва
        :return: bool
        """
        if user.user.is_anonymous:
            return False

        review = Review(user=user,
                        product=product,
                        text=text)
        _repository.save(review=review)
        return True

    @staticmethod
    def product_reviews_list(product: Product, count=None):
        """
        Получение списка отзывов к товару

        :param count: количество отзывов
        :param product: объект Product, у которого берем отзывы
        :return: QuerySet
        """
        if count is not None:
            return _repository.get_all_reviews(
                product=product,
                count=count)
        return _repository.get_all_reviews(product=product)

    @staticmethod
    def product_reviews_amount(product: Product) -> int:
        """
        Получение количества отзывов для товара

        :param product: объект Product, у которого находим кол-во отзывов.

        :return: int
        """

        return _repository.get_amount_reviews(product=product)
