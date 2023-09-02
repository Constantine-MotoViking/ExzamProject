from django.urls import path, re_path
from .views import *

urlpatterns = [
    re_path('dress', dress),
    re_path('wishlist', wishlist),
]
