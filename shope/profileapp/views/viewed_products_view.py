from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from repositories import ViewedProductsRepository


viewed_rep = ViewedProductsRepository()


class ViewedProductsListView(LoginRequiredMixin, ListView):
    """
    View класс для отображения просмотренных продуктов
    """
    template_name = 'profileapp/viewed_products.html'

    def get_queryset(self):
        return viewed_rep.get_viewed_products_by_user(user=self.request.user)
