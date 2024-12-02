from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from myApp.models import Product
from django.conf import settings
# Create your models here.
from django.db.models.signals import post_save


class ShippingAdd(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True )
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    province = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=100)
    country = models.CharField(max_length=100, null=True, blank=True)

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True )
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    shipping_Address = models.TextField(max_length=5500)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    is_shipped = models.BooleanField(default=False)
    def __str__(self):
        return f'Order - {str(self.id)}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True )
    
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f'Order Item - {str(self.id)}'
    


class userPayment(models.Model):
    app_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_checkout_id = models.CharField(max_length=255, unique=True)
    payment_bool = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment by {self.app_user}"

@receiver(post_save, sender=User)
def create_user_payment(sender, instance, created, **kwargs):
    if created:
        userPayment.objects.create(app_user=instance)

    
