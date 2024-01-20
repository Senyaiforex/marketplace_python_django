from interfaces.product_image_interface import ProductImageInterface
from productsapp.models.images import ProductImage
from productsapp.models.product import Product
from django.db.models import QuerySet


class ProductImageRepository(ProductImageInterface):

    def get_all_images(self, product: Product) -> QuerySet[ProductImage]:
        """Получить все изображения данного продукта"""
        return ProductImage.objects.filter(product=product)
