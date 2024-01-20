from coreapp.utils.products_comparison_list import ProductsComparisonList
from repositories import CategorySelectRepository


def count_comparis_block(request):
    """
    Контекстный процессор для отображения
    количества товаров в списке сравнения
    """

    _comparison_service = ProductsComparisonList()
    count_comparis = _comparison_service.comparison_list_size(
        request=request
    )
    context = {
        "count_comparis": count_comparis
    }

    return context


rep_category = CategorySelectRepository()


def categories_list(request):
    """
    Контекстный процессор для вывода категорий в выпадающем списке
    """
    categories = rep_category.non_empty_categories()
    context = {'categories_list': categories}

    return context
