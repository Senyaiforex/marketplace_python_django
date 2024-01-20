from django.urls import path
from cartapp.views import (
    CartItemListView,
    AddToCartAjaxView,
    ReduceFromCartAjaxView,
    DeleteCartItemAjaxView,
    ChangeQuantityCartAjaxView
)

app_name = 'cartapp'
urlpatterns = [
    path('',
         CartItemListView.as_view(), name='cart'),
    path('catalog/ajax_add/',
         AddToCartAjaxView.as_view(), name='ajax_add_product'),
    path('catalog/ajax_reduce/',
         ReduceFromCartAjaxView.as_view(), name='ajax_reduce_product'),
    path('catalog/ajax_delete/',
         DeleteCartItemAjaxView.as_view(), name='ajax_delete_product'),
    path('catalog/ajax_change-count/',
         ChangeQuantityCartAjaxView.as_view(), name='ajax_change_count'),
]
