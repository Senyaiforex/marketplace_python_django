from django.contrib import admin
from productsapp.models.discount import \
    ProductDiscount, SetDiscount, CartDiscount


class ProductInline(admin.StackedInline):
    model = ProductDiscount.products.through
    extra = 0


class CategoryInline(admin.StackedInline):
    model = ProductDiscount.categories.through
    extra = 0


class ProductSetInline(admin.StackedInline):
    model = SetDiscount.products.through
    extra = 0


@admin.register(ProductDiscount)
class AdminProductDiscount(admin.ModelAdmin):
    inlines = [
        ProductInline, CategoryInline
    ]
    list_display = ['name', 'value', 'start_date',
                    'expiration_date', 'priority']


@admin.register(SetDiscount)
class AdminSetDiscount(admin.ModelAdmin):
    inlines = [
        ProductSetInline,
    ]
    list_display = ['name', 'value', 'start_date',
                    'expiration_date', 'priority']


@admin.register(CartDiscount)
class AdminCartDiscount(admin.ModelAdmin):
    list_display = ['name', 'value', 'start_date', 'expiration_date',
                    'priority', 'required_sum', 'required_quantity']
