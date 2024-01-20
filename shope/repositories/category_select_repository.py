from interfaces import CategorySelectInterface
from django.db.models import QuerySet, Count
from productsapp.models import Category


class CategorySelectRepository(CategorySelectInterface):

    def non_empty_categories(self) -> QuerySet[Category]:
        """Получить список всех категорий, в которых есть товары"""
        return Category.objects.annotate(
            prod_amount=Count('category_products')).filter(prod_amount__gt=0)
