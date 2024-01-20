from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from repositories import OrderRepository, OrderItemSelectRepository

order_rep = OrderRepository()
orderitem_rep = OrderItemSelectRepository()


class OrderDetailView(LoginRequiredMixin, DetailView):
    """ Класс-view для детальной информации по заказу """

    template_name = 'orderapp/oneorder.html'

    def get_object(self, queryset=None):
        order = order_rep.get_order_by_id(self.kwargs['order_pk'])
        return order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = order_rep.get_order_by_id(self.kwargs['order_pk'])
        order_items = orderitem_rep.get_all_items(order)
        context['order_items'] = order_items

        return context
