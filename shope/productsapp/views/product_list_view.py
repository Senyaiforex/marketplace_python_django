from django.views.generic import ListView
from productsapp.forms.catalog_filter_form import CatalogFilterForm
from repositories.product_select_repository import ProductSelectRepository
from repositories.tag_select_repository import TagSelectRepository
from django.http import HttpResponseRedirect
from django.core.cache import cache

select_repo = ProductSelectRepository()
tag_repo = TagSelectRepository()


class ProductListView(ListView):
    """ Класс-view для каталога """
    template_name = 'productsapp/catalog.html'
    paginate_by = 3
    extra_context = {'tags_list': tag_repo.get_all_tags()}

    def get(self, request, **kwargs):
        query = request.GET.copy()
        for key in query:  # удаление повторяющихся get-параметров
            query[key] = query.get(key)
        # редирект, когда есть повторяющиеся параметры
        if request.GET != query:
            return HttpResponseRedirect(f'{request.path}?{query.urlencode()}')

        return super().get(request, **kwargs)

    def get_queryset(self):
        if cache.get("catalog"):
            queryset = cache.get("catalog")
        else:
            queryset = select_repo.get_all_products()
            cache.set("catalog", queryset, 60 * 60 * 24)

        form = CatalogFilterForm(self.request.GET)
        if form.is_valid():

            price_min = form.cleaned_data.get('price_min')
            price_max = form.cleaned_data.get('price_max')
            tag = form.cleaned_data.get('tag')
            sort = form.cleaned_data.get('sort')
            query = form.cleaned_data.get('query')
            category = form.cleaned_data.get('category')
            free_delivery = form.cleaned_data.get('free_delivery')
            in_stock = form.cleaned_data.get('in_stock')
            discounted = form.cleaned_data.get('discounted')

            if tag:  # поиск по тегу
                queryset = select_repo.get_products_with_tag(tag=tag)

            else:  # поиск по имени и доп. параметрам
                queryset = select_repo.get_products_with_filter(
                    query=query,
                    category=category,
                    free_delivery=free_delivery,
                    in_stock=in_stock,
                    discounted=discounted)

            queryset = select_repo.get_product_prices(queryset)

            if price_min:  # ограничение выборки по цене, если диапазон задан
                queryset = select_repo.set_price_range(products=queryset,
                                                       price_min=price_min,
                                                       price_max=price_max)

            queryset = select_repo.get_sorted(products=queryset, sort=sort)

        return queryset
