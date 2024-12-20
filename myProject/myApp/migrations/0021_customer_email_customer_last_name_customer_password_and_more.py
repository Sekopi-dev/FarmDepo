# Generated by Django 5.1.2 on 2024-12-05 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0020_remove_customer_email_remove_customer_last_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='email',
            field=models.EmailField(default='not provided', max_length=100),
        ),
        migrations.AddField(
            model_name='customer',
            name='last_name',
            field=models.CharField(default='not provided', max_length=50),
        ),
        migrations.AddField(
            model_name='customer',
            name='password',
            field=models.CharField(default='not provided', max_length=100),
        ),
        migrations.AddField(
            model_name='customer',
            name='phone',
            field=models.CharField(default='not provided', max_length=50),
        ),
    ]
