# Generated by Django 5.1.2 on 2024-12-05 06:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0016_remove_product_dimensions_remove_product_fuel_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='descript',
        ),
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.RemoveField(
            model_name='product',
            name='is_sale',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='sale_price',
        ),
    ]