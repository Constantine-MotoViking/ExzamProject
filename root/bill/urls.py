from django.urls import path, re_path
from .views import *

urlpatterns = [
    re_path('checkout', checkout),
    re_path('cart', cart),
    path('ajax_cart', ajax_cart),
    path('ajax_wish', ajax_wish),
    path('check_wishlist', check_wishlist),
    path('remove_from_wishlist', remove_from_wishlist),
    path('ajax_cart_display', ajax_cart_display),
    path('liqpay_payment/', liqpay_payment, name='liqpay_payment'),
]
