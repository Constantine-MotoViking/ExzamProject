from django.urls import path, re_path
from .views import *

urlpatterns = [
    re_path('checkout', checkout),
    path('liqpay_payment/', liqpay_payment, name='liqpay_payment'),
]
