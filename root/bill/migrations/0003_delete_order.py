# Generated by Django 4.2.3 on 2023-09-02 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0002_order'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]
