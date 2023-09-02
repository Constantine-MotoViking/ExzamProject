from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product


class Transaction(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    title = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(max_length=300)


class Wish(models.Model):
    class Meta:
        verbose_name_plural = "Wishes"

    title = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(max_length=300)

    def str(self) -> str:
        return str(self.title)