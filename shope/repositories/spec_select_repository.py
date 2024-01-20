from django.db.models import QuerySet

from interfaces import SpecificSelectInterface
from productsapp.models import Product,  Specific


class SpecificSelectRepository(SpecificSelectInterface):

    def get_specific_by_product(self, product: Product) -> QuerySet[Specific]:
        specifics = Specific.objects.filter(product=product)
        return specifics
