# Generated by Django 5.1.2 on 2024-12-04 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0006_alter_customer_phone_alter_order_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='dimensions',
            field=models.CharField(blank=True, default='Not Specified', max_length=250),
        ),
        migrations.AlterField(
            model_name='product',
            name='warranty',
            field=models.CharField(blank=True, default='No Warranty', max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight',
            field=models.CharField(blank=True, default='Not Specified', max_length=50),
        ),
    ]