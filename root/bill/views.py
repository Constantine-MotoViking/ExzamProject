from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from liqpay import LiqPay
from django.views.decorators.csrf import csrf_exempt
import json
import hashlib
import base64


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

        public_key = 'sandbox_i48179431932'
        private_key = 'sandbox_thk0aoKFXarAROfllj6S0u1SCZIjq8LPU1cVvZq8'

        data = {
            'action': 'pay',
            'amount': amount,
            'currency': 'UAH',
            'description': description,
            'order_id': order_id,
            'version': '3',
            'public_key': public_key,
        }

        # Формуємо підпис для даних
        data_encoded = base64.b64encode(json.dumps(data).encode())
        signature = base64.b64encode(hashlib.sha1(f"{private_key}{data_encoded}{private_key}".encode()).digest())

        return HttpResponse()
    else:
        return HttpResponseBadRequest("Метод не дозволений")


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