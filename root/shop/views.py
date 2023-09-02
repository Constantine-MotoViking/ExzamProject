from django.shortcuts import render
from catalog.models import *


def dress(request):
    return render(request, 'shop/dress.html', {
        'title': 'Сукні',
        'page': 'dress',
        'app': 'shop',
        'all_categories': Category.objects.all(),
        'all_products': Product.objects.all()
    })


