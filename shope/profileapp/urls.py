from django.urls import path
from .views import ProfileDetailView, ProfileUpdateView, ViewedProductsListView

app_name = 'profileapp'

urlpatterns = [
    path('account/', ProfileDetailView.as_view(), name='account'),
    path('profile/', ProfileUpdateView.as_view(), name='profile_update'),
    path('viewed/', ViewedProductsListView.as_view(), name='viewed_products'),
]
