from django.urls import path
from django.views.decorators.cache import cache_page

from productsapp.views import (
    ProductListView,
    AddReviewView,
    ProductComparisonView,
    ProductDetailView,
    AddToComparisonView,
    RemoveFromComparisonView,
    export_product_to_xls,
    DiscountsListView,
    DiscountSetDetailView,
    DiscountCartDetailView,
    seller_detail_view,
)

app_name = 'productsapp'

urlpatterns = [
    path('catalog/', ProductListView.as_view(), name="catalog"),
    path('catalog/<int:product_id>/', ProductDetailView.as_view(), name="product_detail"),
    path('catalog/<int:product_id>/add_review/', AddReviewView.as_view(), name="add_review"),
    path('catalog/<int:product_id>/add_to_comparison/', AddToComparisonView.as_view(), name="add_to_comparison"),
    path('catalog/export/', export_product_to_xls, name="export_product"),
    path('comparison/', ProductComparisonView.as_view(), name="comparison"),
    path('comparison/<int:product_id>', RemoveFromComparisonView.as_view(), name="remove_from_comp"),
    path('sale/', DiscountsListView.as_view(), name="sales"),
    path('sale/<int:elem_id>/set/', DiscountSetDetailView.as_view(), name="discount_set_detail"),
    path('sale/<int:elem_id>/cart/', DiscountCartDetailView.as_view(), name="discount_cart_detail"),
    path('sellers/<int:seller_id>/', cache_page(timeout=86400,
                                                key_prefix="seller_detail"
                                                )(seller_detail_view), name="seller_detail"),
]
