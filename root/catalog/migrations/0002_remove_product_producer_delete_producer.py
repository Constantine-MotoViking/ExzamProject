# Generated by Django 4.2.3 on 2023-09-02 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='producer',
        ),
        migrations.DeleteModel(
            name='Producer',
        ),
    ]
