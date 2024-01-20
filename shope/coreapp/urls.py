from django.urls import path
from .views import IndexView

app_name = 'coreapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    # path('clear_cache/<str:cache_name>', clear_cache, name="clear_cache"),
]
