from django.urls import path, re_path
from .views import *

urlpatterns = [
    re_path('checkout', checkout),
    path('ajax_cart', ajax_cart),
    path('ajax_cart_display', ajax_cart_display),
    path('liqpay_payment/', liqpay_payment, name='liqpay_payment'),
]
