from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('sign_up', sign_up),
    path('sign_in', sign_in),
    re_path('sign_out', sign_out),
    re_path('profile', profile),
    re_path('prof_wish', prof_wish),
    path('ajax_reg', ajax_reg),
    path('sign_up_in', sign_up_in)
]
