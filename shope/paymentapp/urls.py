from django.urls import path
from paymentapp.views import PaymentView

app_name = 'paymentapp'

urlpatterns = [
    path('<int:order_pk>', PaymentView.as_view(), name='payment'),
]
