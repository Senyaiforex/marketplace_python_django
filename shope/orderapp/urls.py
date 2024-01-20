from django.urls import path
from orderapp.views import OrderListView, OrderDetailView, \
    AddOrderView, export_orders_to_xls, EditOrderView, RemoveOrderItemView


app_name = 'orderapp'

urlpatterns = [

    path('', AddOrderView.as_view(), name='add_order'),
    path('editorder/<int:order_pk>/', EditOrderView.as_view(), name='edit_order'),
    path('removeitem/<int:order_pk>/<int:orderitem_pk>/', RemoveOrderItemView.as_view(), name='remove_item'),
    path('historyorder/', OrderListView.as_view(), name='history_order'),
    path('oneorder/<int:order_pk>/', OrderDetailView.as_view(), name='oneorder'),
    path('historyorder/export_orders/', export_orders_to_xls, name='export_orders'),
]
