from django.shortcuts import render
from django.http import HttpResponse
from liqpay import LiqPay
from django.views.decorators.csrf import csrf_exempt
import json


def checkout(request):
    return render(request, 'bill/checkout.html', {
        'title': 'Замовлення',
        'page': 'checkout',
        'app': 'bill',
    })


def liqpay_payment(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        amount = request.POST.get('amount')
        description = request.POST.get('description')

        liqpay = LiqPay(
            public_key='YOUR_PUBLIC_KEY',
            private_key='YOUR_PRIVATE_KEY',
        )

        params = {
            'action': 'pay',
            'amount': amount,
            'currency': 'UAH',
            'description': description,
            'order_id': order_id,
            'result_url': 'https://yourwebsite.com/payment/success/',
        }

        # Генеруємо підпис
        signature = liqpay.cnb_signature(params)

        # Додаємо підпис до параметрів
        params['signature'] = signature

        # Створюємо форму для переходу до оплати
        form = liqpay.cnb_form(params)

        return HttpResponse(form)
    else:
        return HttpResponse("Метод не дозволений")


@csrf_exempt
def liqpay_callback(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        # Отримайте дані про оплату з callback
        order_id = data.get('order_id')
        payment_status = data.get('status')

        # Оновіть статус оплати в базі даних

        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)