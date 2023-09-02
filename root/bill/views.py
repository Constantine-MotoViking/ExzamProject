from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.utils import timezone
from django.core.mail import send_mail
from liqpay import LiqPay
from .models import Order
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


def ajax_cart(request):
    response = dict()
    response['message'] = 'Привіт від сервера!'

    # 1 - Отримуємо значення get-параметрів від кліента
    uid = request.GET.get('uid')
    pid = request.GET.get('pid')
    price = request.GET.get('price')

    # 2 - Створюємо нове замовлення та зберігаемо його в БД:
    Order.objects.create(
        title=f'Order-{pid}/{uid}/{timezone.now()}',
        user_id=uid,
        product_id=pid,
        amount=float(price),
        notes='Очікує підтвердження'
    )

    # 3 - Зчитуємо із бази список всіх замовлень даного користувача:
    user_orders = Order.objects.filter(user_id=uid)

    # 4 - Обчислюємо загальну вартість всіх замовлень даного користувача:
    amount = 0
    for order in user_orders:
        amount += order.amount

    # 5 - Записуємо у відповідь сервера загальну вартість та кількість товарів:
    response['amount'] = amount
    response['count'] = len(user_orders)

    return JsonResponse(response)


def ajax_cart_display(request):
    # 1
    response = dict()
    response['message'] = 'AJAX-OK'

    # 2
    uid = request.GET.get('uid')
    response['uid'] = uid

    # 3
    user_products = Order.objects.filter(user_id=uid)
    amount = 0

    # 4
    for product in user_products:
        amount += product.amount

    # 5
    response['count'] = len(user_products)
    response['total'] = amount

    return JsonResponse(response)
