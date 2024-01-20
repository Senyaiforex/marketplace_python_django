from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from repositories import OrderRepository

order_rep = OrderRepository()


class OrderListView(LoginRequiredMixin, ListView):
    """ Класс-view для заказов """

    template_name = 'orderapp/historyorder.html'
    ordering = '-created_at'

    def get_queryset(self):
        return order_rep.get_all_by_user(self.request.user.id)
