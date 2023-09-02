from django.db import models


class Transaction(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    order_id = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20)


