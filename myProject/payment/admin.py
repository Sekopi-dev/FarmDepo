from django.contrib import admin
from .models import ShippingAdd, Order, OrderItem, userPayment
from django.contrib.auth.models import User


admin.site.register(ShippingAdd)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(userPayment)

#
class OrderItemInLine(admin.StackedInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    model = OrderItem
    readonly_fields = ["date_ordered"]
    inlines = [OrderItemInLine]
# Register your models here.

admin.site.unregister(Order)

admin.site.register(Order, OrderAdmin)


