from django.contrib import admin
from authapp.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Регистрация модели в админ-панели
    """
    list_display = [
        'id', 'username', 'first_name',
        'last_name', 'middle_name', 'email',
        'is_staff', 'is_active', 'date_joined',
    ]  # отображаемые поля в админ-панели
    search_fields = ['username',
                     'first_name',
                     'last_name'
                     ]  # поля, по которым будет идти поиск

# Register your models here.
