from django.shortcuts import render


def dress(request):
    return render(request, 'shop/dress.html', {
        'title': 'Сукні',
        'page': 'dress',
        'app': 'shop',
    })
