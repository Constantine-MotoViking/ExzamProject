from django.urls import path
from .views import *

urlpatterns = [
    path('checkout', checkout),
    path('liqpay_payment/', liqpay_payment, name='liqpay_payment'),
]
