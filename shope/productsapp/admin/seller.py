from django.contrib import admin

from productsapp.models import Seller
from authapp.models import User


class SellerAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(SellerAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def render_change_form(self, request, context, *args, **kwargs):
        """
        Настройка отображения страницы редактирования позиции
        """
        if not request.user.is_superuser:
            context['adminform'].form.fields[
                'owner'].queryset = User.objects.filter(pk=request.user.id)
        return super(SellerAdmin, self).render_change_form(
            request, context, *args, **kwargs)


admin.site.register(Seller, SellerAdmin)
