from . import views 
from django.urls import path


urlpatterns = [
path('payment_success', views.payment_success, name="payment_success"),
path('checkout', views.checkout, name="checkout"),
path('billing', views.billing, name="billing"),
path('pay_now', views.pay_now, name="pay_now"),
path('process_order', views.process_order, name="process_order"),
path('payment_cancel', views.payment_cancelled, name="payment_cancel"),
path('stripe_webhook', views.stripe_webhook, name='stripe_webhook'),
path('payment_successful', views.payment_successful, name="payment_successful"),
# path('create_checkout_session', views.create_checkout_session, name="create_checkout_session"),

path('checkout_session/', views.create_checkout_session, name='checkout_session'),  # Checkout URL

]