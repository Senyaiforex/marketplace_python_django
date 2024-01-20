from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from coreapp.utils import ViewedProductsService
from coreapp.utils.add_product_review import AddProductReview
from coreapp.utils.products_comparison_list import ProductsComparisonList
from productsapp.forms import AddReviewForm
from repositories import SellerSelectRepository, \
    SpecificSelectRepository, ProductSelectRepository
from repositories.price_repository import PriceRepository
from repositories.product_image_repository import ProductImageRepository

_select_seller_repo = SellerSelectRepository()
_select_specifics_repo = SpecificSelectRepository()
_price_repository = PriceRepository()
_product_image_repo = ProductImageRepository()
_product_repo = ProductSelectRepository()


class AddToComparisonView(View):
    """
    Представление для добавления товара в список сравнения
    """

    _comparison_service = ProductsComparisonList()
    _review_service = AddProductReview()
    _viewed_service = ViewedProductsService()

    template_name = "productsapp/product.html"
    form_class = AddReviewForm

    def get(self, request: HttpRequest, product_id: int) -> HttpResponse:
        product = _product_repo.get_product_by_id(product_id)
        # получаем конкретный продукт
        product_price = _price_repository. \
            get_min_price_object(product=product)
        amount_review = self._review_service.product_reviews_amount(product=product)
        # количество отзывов
        reviews_list = self._review_service.product_reviews_list(
            product=product,
            count=1)
        # список отзывов
        sellers = _select_seller_repo.get_seller_by_product(
            product=product
        )
        specifics = _select_specifics_repo.get_specific_by_product(
            product=product
        )
        if request.user.is_authenticated:
            self._viewed_service.add_to_viewed_products(
                user=request.user,
                product=product
            )

        product_images = _product_image_repo.get_all_images(product=product)

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

        product = _product_repo.get_product_by_id(product_id)
        product_images = _product_image_repo.get_all_images(product=product)
        product_price = _price_repository. \
            get_min_price_object(product=product)
        amount_review = self._review_service.product_reviews_amount(product=product)
        reviews_list = self._review_service.product_reviews_list(product=product)
        category_in_comp = self._comparison_service.\
            get_comparison_list(request).first()
        cur_category = product.category
        error_category = False
        if category_in_comp is None or \
                category_in_comp.category == cur_category:
            self._comparison_service.add_to_comparison(
                request=request,
                product_id=product_id
            )
        elif category_in_comp and \
                category_in_comp.category != cur_category:
            error_category = True

        return render(request, self.template_name,
                      context={"product": product,
                               "product_images": product_images,
                               "product_price": product_price,
                               "amount_review": amount_review,
                               "reviews_list": reviews_list,
                               "form": self.form_class,
                               "error_category": error_category})
