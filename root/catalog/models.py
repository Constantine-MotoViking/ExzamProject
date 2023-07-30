from django.db import models


class Category(models.Model):
    # 1
    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return str(self.name)


class Producer(models.Model):
    # 2
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return str(self.name)


class Product(models.Model):
    # 3
    name = models.CharField(max_length=100)
    about = models.TextField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    photo = models.FileField(upload_to='products/')
    price = models.FloatField()

    def __str__(self) -> str:
        return str(self.name)
