from django.contrib import admin
from cartapp.models.cart import Cart
from cartapp.models.cartitem import CartItem

admin.site.register(Cart)
admin.site.register(CartItem)
