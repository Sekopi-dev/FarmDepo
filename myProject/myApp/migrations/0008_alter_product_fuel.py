# Generated by Django 5.1.2 on 2024-12-04 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0007_alter_product_dimensions_alter_product_warranty_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='fuel',
            field=models.CharField(blank=True, default='N/A', max_length=50),
        ),
    ]
