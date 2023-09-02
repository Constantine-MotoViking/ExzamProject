from django.shortcuts import render


def checkout(request):
    return render(request, 'bill/checkout.html', {
        'title': 'Замовлення',
        'page': 'checkout',
        'app': 'bill',
    })
