from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from django.core.cache import cache

from productsapp.forms import AddReviewForm
from coreapp.utils import ViewedProductsService
from coreapp.utils.add_product_review import AddProductReview
from repositories.price_repository import PriceRepository
from repositories.product_image_repository import ProductImageRepository
from repositories.profile_repository import ProfileRepository
from repositories import SellerSelectRepository, SpecificSelectRepository, ProductSelectRepository

_profile_repository = ProfileRepository()
_select_seller_repo = SellerSelectRepository()
_select_specifics_repo = SpecificSelectRepository()
_price_repository = PriceRepository()
_product_image_repo = ProductImageRepository()
_product_repository = ProductSelectRepository()


class ProductDetailView(View):
    """
    Класс-view для отображения детальной страницы продукта
    """
    _service = AddProductReview()
    _viewed_service = ViewedProductsService()

    template_name = "productsapp/product.html"
    form_class = AddReviewForm

    def get(self, request: HttpRequest, product_id: int) -> HttpResponse:
        total_data = cache.get(f"product_detail_{product_id}")
        if total_data is not None:
            product = total_data.get("product")
            product_price = total_data.get("product_price")
            amount_review = self._service.product_reviews_amount(product=product)
            reviews_list = self._service.product_reviews_list(
                product=product,
                count=1)
            sellers = total_data.get("sellers")
            specifics = total_data.get("specifics")
            product_images = total_data.get("product_images")

        else:
            product = _product_repository.get_product_by_id(product_id=product_id)
            # получаем конкретный продукт
            product_price = _price_repository. \
                get_min_price_object(product=product)
            amount_review = self._service.product_reviews_amount(product=product)
            # количество отзывов
            reviews_list = self._service.product_reviews_list(
                product=product,
                count=1)
            # список отзывов
            sellers = _select_seller_repo.get_seller_by_product(
                product=product
            )
            specifics = _select_specifics_repo.get_specific_by_product(
                product=product
            )

            product_images = _product_image_repo.get_all_images(product=product)

            cache.set(f"product_detail_{product_id}", {
                "product": product,
                "product_price": product_price,
                "sellers": sellers,
                "specifics": specifics,
                "product_images": product_images
            },
                      60 * 60 * 24)

        if request.user.is_authenticated:
            self._viewed_service.add_to_viewed_products(
                user=request.user,
                product=product
            )

        return render(request, self.template_name,
                      context={"product": product,
                               "product_images": product_images,
                               "form": self.form_class,
                               "product_price": product_price,
                               "amount_review": amount_review,
                               "reviews_list": reviews_list,
                               'sellers': sellers,
                               'specifics': specifics,
                               "user": request.user})

    def post(self, request: HttpRequest, product_id: int) -> HttpResponse:
        product = _product_repository.get_product_by_id(product_id=product_id)
        product_images = _product_image_repo.get_all_images(product=product)
        product_price = _price_repository. \
            get_min_price_object(product=product)
        amount_review = self._service.product_reviews_amount(product=product)
        is_show_more = False  # Нажата ли кнопка "Показать еще"
        if "show_more" in request.POST:
            reviews_list = self._service.product_reviews_list(product=product)
            is_show_more = True
        else:
            reviews_list = self._service.product_reviews_list(
                product=product,
                count=1,
            )
        return render(request, self.template_name,
                      context={"product": product,
                               "product_images": product_images,
                               "product_price": product_price,
                               "amount_review": amount_review,
                               "reviews_list": reviews_list,
                               "is_show": is_show_more,
                               "form": self.form_class})
