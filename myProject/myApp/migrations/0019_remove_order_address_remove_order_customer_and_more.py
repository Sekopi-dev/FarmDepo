# Generated by Django 5.1.2 on 2024-12-05 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0018_product_catergory_product_descript_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='order',
            name='date',
        ),
        migrations.RemoveField(
            model_name='order',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='order',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
    ]
