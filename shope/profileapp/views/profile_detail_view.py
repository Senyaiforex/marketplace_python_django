from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from profileapp.models import Profile
from repositories import OrderRepository, ViewedProductsRepository

order_rep = OrderRepository()
viewed_rep = ViewedProductsRepository()


class ProfileDetailView(LoginRequiredMixin, DetailView):
    """
    View класс для отображения информации об аккаунте
    """
    queryset = Profile
    template_name = 'profileapp/account.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = order_rep.get_last_activ(user=self.request.user)
        context['viewed'] = viewed_rep.get_by_user_limit(
            user=self.request.user,
            limit=3
        )
        return context
