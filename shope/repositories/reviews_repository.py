from django.db.models import QuerySet

from interfaces.reviews_interface import ReviewInterface
from productsapp.models import Review, Product


class ReviewRepository(ReviewInterface):

    def get_all_reviews(self,
                        product: Product,
                        count=None) -> QuerySet[Review]:
        if count is not None:
            reviews = product.reviews.all()
            if len(reviews) >= count:
                # Если в списке есть столько элементов, возвращаем срез
                return reviews[:count]
            elif len(reviews) == 0:
                return reviews
            # Иначе ошибка
            else:
                raise IndexError
        return product.reviews.all()

    def get_amount_reviews(self, product: Product) -> int:
        return product.reviews.count()

    def save(self, review: Review, force=None) -> None:
        if force:
            review.save(force)
        review.save()
