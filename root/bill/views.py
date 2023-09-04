from collections import defaultdict
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from liqpay import LiqPay
import json
import base64
import hashlib
from .models import *


@csrf_exempt
def liqpay_payment(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        amount = request.POST.get('amount')
        description = request.POST.get('description')

        public_key = 'sandbox_i48179431932'
        private_key = 'sandbox_thk0aoKFXarAROfllj6S0u1SCZIjq8LPU1cVvZq8'
        sandbox_mode = True  # Включити тестовий режим (True) або вимкнути (False)

        # Параметри для створення платежу
        data = {
            "version": "3",
            "public_key": public_key,
            "action": "pay",
            "amount": amount,
            "currency": "USD",  # Змініть на потрібну валюту
            "description": description,
            "order_id": order_id,
            "result_url": request.build_absolute_uri(reverse('payment_success')),
            # URL для перенаправлення після оплати
            "server_url": request.build_absolute_uri(reverse('liqpay_callback')),
            # URL для отримання callback від LiqPay
        }

        # Якщо включений тестовий режим, додати відповідний прапорець
        if sandbox_mode:
            data["sandbox"] = "1"

        # Підписати дані для відправки в LiqPay
        data = base64.b64encode(json.dumps(data).encode()).decode()
        signature = base64.b64encode(hashlib.sha1(f"{private_key}{data}{private_key}".encode()).digest()).decode()

        return render(request, 'bill/checkout.html', {
            'liqpay_data': data,
            'liqpay_signature': signature,
        })
    else:
        return HttpResponseBadRequest("Метод не дозволений")


@csrf_exempt
def liqpay_callback(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        signature = request.POST.get('signature')

        public_key = 'sandbox_i48179431932'
        private_key = 'sandbox_thk0aoKFXarAROfllj6S0u1SCZIjq8LPU1cVvZq8'

        # Перевірка підпису
        expected_signature = base64.b64encode(
            hashlib.sha1(f"{private_key}{data}{private_key}".encode()).digest()).decode()

        if signature == expected_signature:
            # Якщо підпис вірний, розшифруйте дані
            decoded_data = base64.b64decode(data).decode()
            payment_info = json.loads(decoded_data)

            # Отримайте ідентифікатор замовлення з отриманих даних
            order_id = payment_info.get('order_id')

            # Оновіть статус замовлення в базі даних, наприклад, на "success"
            Order.objects.filter(title=order_id).update(payment_status='success')

            # Можливо, вам також потрібно записати іншу інформацію про платіж

            # Поверніть успішну відповідь, щоб LiqPay зупинив надсилання повідомлень
            return HttpResponse(status=200)
        else:
            # Якщо підпис невірний, поверніть помилку
            return HttpResponseBadRequest("Помилка перевірки підпису")
    else:
        return HttpResponseBadRequest("Метод не дозволений")


def checkout(request):
    all_orders = Order.objects.filter(user_id=request.user.id)
    total_price = sum(order.amount for order in all_orders)

    order_summary = defaultdict(int)

    for order in all_orders:
        order_summary[order.product] += 1

    order_summary_list = [{'product': product, 'quantity': quantity} for product, quantity in order_summary.items()]

    return render(request, 'bill/checkout.html', {
        'title': 'Замовлення',
        'page': 'checkout',
        'app': 'bill',
        'all_orders': all_orders,
        'total_price': total_price,
        'order_summary_list': order_summary_list
    })


def cart(request):
    all_orders = Order.objects.filter(user_id=request.user.id)
    total_price = sum(order.amount for order in all_orders)

    order_summary = defaultdict(int)

    for order in all_orders:
        order_summary[order.product] += 1

    order_summary_list = [{'product': product, 'quantity': quantity} for product, quantity in order_summary.items()]

    context = {
        'all_orders': all_orders,
        'total_price': total_price,
        'order_summary_list': order_summary_list
    }
    return render(request, 'bill/cart.html', context)


def ajax_cart(request):
    response = dict()
    response['message'] = 'Привіт від сервера!'

    # 1 - Отримуємо значення get-параметрів від кліента
    uid = request.GET.get('uid')
    pid = request.GET.get('pid')
    price = request.GET.get('price')
    img = request.GET.get('image')

    # 2 - Створюємо нове замовлення та зберігаемо його в БД:
    Order.objects.create(
        title=f'Order-{pid}/{uid}/{timezone.now()}',
        user_id=uid,
        product_id=pid,
        amount=float(price),
        notes='Очікує підтвердження',
        image=img
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


@csrf_exempt
def ajax_wish(request):
    response = dict()
    response['message'] = 'Привіт від сервера!'

    uid = request.GET.get('uid')
    user_products = Wish.objects.filter(user_id=uid)
    amount = 0

    response['count'] = len(user_products)

    uid = request.GET.get('uid')
    pid = request.GET.get('pid')
    price = request.GET.get('price')
    img = request.GET.get('image')

    Wish.objects.create(
        title=f'Wish-{pid}/{uid}/{timezone.now()}',
        user_id=uid,
        product_id=pid,
        amount=float(price),
        notes='Додано до списку бажаного',
        image=img
    )

    return JsonResponse(response)


@csrf_exempt
def check_wishlist(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        product_id = request.GET.get('product_id')

        # Перевірте, чи товар знаходиться в обраному для даного користувача
        is_in_wishlist = Wish.objects.filter(user_id=user_id, product_id=product_id).exists()

        response = {'is_in_wishlist': is_in_wishlist}
        return JsonResponse(response)


@csrf_exempt
def remove_from_wishlist(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        product_id = request.POST.get('product_id')

        try:
            # Видаліть товар зі списку обраного на стороні сервера
            # Використовуйте Django ORM для цього
            Wish.objects.filter(user_id=user_id, product_id=product_id).delete()

            # Поверніть відповідь, яка містить оновлену кількість товарів в обраному
            user_products = Wish.objects.filter(user_id=user_id)
            response = {'message': 'Товар успішно видалено з обраного', 'count': len(user_products)}

            return JsonResponse(response)
        except Exception as e:
            return JsonResponse({'message': 'Помилка при видаленні товару з обраного'})
    else:
        return JsonResponse({'message': 'Недопустимий метод запиту'})
