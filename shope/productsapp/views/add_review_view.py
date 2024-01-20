from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from productsapp.forms import AddReviewForm
from coreapp.utils.add_product_review import AddProductReview
from repositories.price_repository import PriceRepository
from repositories.product_select_repository import ProductSelectRepository
from repositories.profile_repository import ProfileRepository
from repositories import SellerSelectRepository, SpecificSelectRepository

_profile_repository = ProfileRepository()
_product_repository = ProductSelectRepository()
select_seller_repo = SellerSelectRepository()
select_specifics_repo = SpecificSelectRepository()
_price_repository = PriceRepository()


class AddReviewView(View):
    """
    Класс-view для добавления отзыва к продукту
    """
    form_class = AddReviewForm
    _service = AddProductReview()

    def post(self,
             request: HttpRequest,
             product_id: int) -> HttpResponse:
        form = self.form_class(data=request.POST)  # форма с отзывом
        product = _product_repository.get_product_by_id(
            product_id=product_id
        )
        if request.user.is_authenticated:
            if form.is_valid():
                # Если форма валидна и юзер авторизован, берем отзыв и добавляем к продукту.
                text = form.cleaned_data.get("text")
                self._service.add_product_review(
                    user=_profile_repository.get_profile(request.user),
                    product=product,
                    text=text
                )
        return redirect(reverse("productsapp:product_detail",
                                kwargs={"product_id": product.pk}))
