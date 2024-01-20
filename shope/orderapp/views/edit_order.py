from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from orderapp.forms import OrderForm
from paymentapp.forms import PaymentForm
from repositories import OrderRepository, OrderItemSelectRepository

order_rep = OrderRepository()
orderitem_rep = OrderItemSelectRepository()


class EditOrderView(LoginRequiredMixin, View):
    """Класс-view для редактирования заказа"""

    template_name = 'orderapp/order.html'

    def get(self, request, **kwargs):
        order = order_rep.get_order_by_id(kwargs['order_pk'])
        order_items = orderitem_rep.get_all_items(order=order)

        # Предзаполняем заказ данными из профиля
        if not (order.fio and order.phone_number):
            if request.user.profile.fio.strip():
                order.fio = request.user.profile.fio
            order.phone_number = request.user.profile.phone_number

        order_form = OrderForm(instance=order)

        payment_form = PaymentForm()
        payment_form.fields[
            'total_sum'].initial = order.total_discounted_price

        context = {
            'order_form': order_form,
            'payment_form': payment_form,
            'order': order,
            'order_items': order_items,
        }
        return render(request, self.template_name, context)
