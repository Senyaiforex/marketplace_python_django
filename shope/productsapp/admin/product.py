from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path

from productsapp.models.product import Product
from shope.tasks import import_run  # noqa


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Регистрация модели Product в админ-панели
    """
    list_display = ["pk",
                    "name",
                    "description",
                    "tags",
                    "archived",
                    "free_delivery",
                    "category",
                    ]

    ordering = "name", "archived", "free_delivery"
    change_list_template = "productsapp/button_to_start_importing.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "run_background_imports/",
                self.admin_site.admin_view(
                    self.run_background_imports_view,
                ),
                name="run_background_imports"
            ),
        ]
        return custom_urls + urls

    def run_background_imports_view(self, request):
        import_run.delay()
        return HttpResponseRedirect("../")
