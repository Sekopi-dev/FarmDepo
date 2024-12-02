from django.db import models
import datetime

class Catergory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    class Meta: 
        verbose_name_plural = 'categories'

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return f' {self.first_name}{self.last_name}'
        

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(default=0,decimal_places=2,max_digits=6 )
    catergory = models.ForeignKey(Catergory, on_delete=models.CASCADE, default=1)
    descript = models.CharField(max_length=250, default='No Description', blank=True)
    image = models.ImageField(upload_to='uploads/products/')
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0,decimal_places=2,max_digits=6 )

    
    weight = models.CharField(max_length=20, default='Not Specified', blank=True)
    dimensions = models.CharField(max_length=50, default='Not Specified', blank=True)
    material =  models.CharField(max_length=250, default='Not Specified', blank=True)
    fuel = models.CharField(max_length=250, default='N/A', blank=True)
    warranty = models.CharField(max_length=20, default='No Warranty', blank=True)
    def __str__(self):   
        return self.name

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE, default=1 )
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=20, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):   
        return self.product
