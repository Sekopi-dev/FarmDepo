from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from myApp.models import Product
from django.conf import settings
from django.db.models.signals import post_save


class ShippingAdd(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100, default="John Doe")
    email = models.EmailField(max_length=100, default="example@example.com")
    address1 = models.CharField(max_length=250, default="123 Main Street")
    address2 = models.CharField(max_length=250, default="Apt 101")
    city = models.CharField(max_length=250, default="New York")
    province = models.CharField(max_length=100, null=True, blank=True, default="New York")
    code = models.CharField(max_length=100, default="10001")
    country = models.CharField(max_length=100, null=True, blank=True, default="USA")

    class Meta:
        verbose_name_plural = "shipping Address"

    def __str__(self):
        return f'Shipping Address - {str(self.id)}'


def create_shipping(sender, instance, created, **kwargs):
    if created:
        user_address = ShippingAdd(user=instance)
        user_address.save()
post_save.connect(create_shipping, sender=User)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100, default="John Doe")
    email = models.EmailField(max_length=100, default="example@example.com")
    shipping_Address = models.TextField(max_length=5500, default="123 Main Street, Apt 101, New York, USA")
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_ordered = models.DateTimeField(auto_now_add=True)
    is_shipped = models.BooleanField(default=False)

    def __str__(self):
        return f'Order - {str(self.id)}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'Order Item - {str(self.id)}'


class userPayment(models.Model):
    app_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_checkout_id = models.CharField(max_length=255, unique=True, default="default_checkout_id")
    payment_bool = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment by {self.app_user}"


@receiver(post_save, sender=User)
def create_user_payment(sender, instance, created, **kwargs):
    if created:
        userPayment.objects.create(app_user=instance)
