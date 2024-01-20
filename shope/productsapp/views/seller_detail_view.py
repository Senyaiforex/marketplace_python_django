from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from repositories import SellerSelectRepository, ProductSelectRepository, PriceRepository
from django.core.cache import cache

_seller_repository = SellerSelectRepository()
_product_repository = ProductSelectRepository()
_price_repository = PriceRepository()


def seller_detail_view(request: HttpRequest, seller_id: int) -> HttpResponse:
    """ Представление для детальной страницы продавца """
    seller, products = cache.get(f"seller_detail_{seller_id}"), cache.get(f"products_top_{seller_id}")
    if seller is None:
        seller = _seller_repository.get_seller(seller_id=seller_id)
        cache.set(f"seller_detail_{seller_id}", seller, 60 * 60 * 24)
    if products is None:
        products = _product_repository.get_products_by_seller_id(seller_id=seller_id)
        cache.set(f"products_top_{seller_id}", products, 60 * 60)
    for product in products:
        product.price = _price_repository.get_price(product, seller)

    return render(request, "productsapp/detailed_seller.html", {"seller": seller,
                                                                "products": products})
