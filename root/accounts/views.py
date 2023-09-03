from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bill.models import *


def sign_up(request):
    if request.method == 'GET':
        return render(request, 'users/signup.html', context={
            'page_title': 'Реєстрація'
        })
    elif request.method == 'POST':
        login_x = request.POST.get('login')
        pass1_x = request.POST.get('pass1')
        email_x = request.POST.get('email')

        user = User.objects.create_user(login_x, email_x, pass1_x)
        user.save()

        color = 'red'
        report = 'В реєстрації відмовлено!'
        if user is not None:
            color = 'green'
            report = 'Реєстрація успішно завершена!'

        return render(request, 'users/reports.html', context={
            'page_title': 'Звіт про реєстрацію',
            'color': color,
            'report': report
        })


@csrf_exempt
def sign_in(request):
    if request.method == 'GET':
        return render(request, 'users/signin.html', context={
            'page_title': 'Авторизація'
        })
    elif request.method == 'POST':
        login_x = request.POST.get('login')
        pass1_x = request.POST.get('pass1')

        user = authenticate(request, username=login_x, password=pass1_x)

        color = 'red'
        report = 'Користувач не знайдений!'
        if user is not None:
            color = 'green'
            report = 'Вхід виконано успішно!'
            login(request, user)

        return render(request, 'users/profile.html', context={
            'page_title': 'Обліковий запис',
        })


def sign_out(request):
    logout(request)
    return redirect('/')


def profile(request):
    all_orders = Order.objects.all()
    context = {
        'page_title': 'Профіль користувача',
        'all_orders': all_orders
    }
    return render(request, 'users/profile.html', context)


def sign_up_in(request):
    return render(request, 'users/sign_up_in.html', context={
        'page_title': 'Сторінка входу/реєстрації'
    })


def ajax_reg(request):
    response = dict()
    login = request.GET.get('login')
    email = request.GET.get('email')
    try:
        User.objects.get(username=login)
        response['login_message'] = 'зайнятий'
    except User.DoesNotExist:
        response['login_message'] = 'вільний'

    try:
        User.objects.get(email=email)
        response['email_message'] = 'зайнятий'
    except User.DoesNotExist:
        response['email_message'] = 'вільний'

    return JsonResponse(response)
