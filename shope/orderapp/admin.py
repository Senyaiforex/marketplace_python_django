from django.contrib import admin
from orderapp.models import Order, OrderItem

admin.site.register(Order)
admin.site.register(OrderItem)
