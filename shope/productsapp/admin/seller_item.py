from django.contrib import admin

from productsapp.models import SellerItem, Seller


class SellerItemAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        """
        Настройка вывода только тех позиций,
        которые принадлежат текущему пользователю
        """
        qs = super(SellerItemAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(seller__owner=request.user)

    def render_change_form(self, request, context, *args, **kwargs):
        """
        Настройка отображения страницы редактирования позиции
        """
        if not request.user.is_superuser:
            context['adminform'].form.fields[
                'seller'].queryset = Seller.objects.filter(owner=request.user)
        return super(SellerItemAdmin, self).render_change_form(
            request, context, *args, **kwargs)


admin.site.register(SellerItem, SellerItemAdmin)
