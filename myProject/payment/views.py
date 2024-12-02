from django.shortcuts import render, redirect
from cart.cart import Cart

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from payment.models import userPayment
import stripe
import time

stripe.api_key = settings.STRIPE_SECRET_KEY

from payment.forms import ShippingForm, paymentForm
from payment.models import ShippingAdd, Order, OrderItem
from django.contrib.auth.models import User
from myApp.models import Product
# Create your views here.

def payment_success(request):
    return render(request, "payment/payment_success.html", {})

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    prod_quant = cart.get_quant
    totals = cart.total
    
    if request.user.is_authenticated:
        # shipping_user = ShippingAdd.objects.get(id = request.user.id)
        shipping_user = ShippingAdd.objects.get(user=request.user)

        ship_form = ShippingForm(request.POST or None, instance=shipping_user, )
        return render(request, "payment/checkout.html", {"cart_products": cart_products, "quantity": prod_quant, "totals": totals, 'ship_form': ship_form })
    else:
        ship_form = ShippingForm(request.POST or None, )
        return render(request, "payment/checkout.html", {"cart_products": cart_products, "quantity": prod_quant, "totals": totals, 'ship_form': ship_form })

def billing(request):
    cart = Cart(request)
    if request.method == 'POST':
        # Save shipping info to session
        my_shipping = {
            'shipping_fullname': request.POST.get('shipping_fullname'),
            'shipping_email': request.POST.get('shipping_email'),
            'shipping_address1': request.POST.get('shipping_address1'),
            'shipping_address2': request.POST.get('shipping_address2'),
            'shipping_city': request.POST.get('shipping_city'),
            'shipping_province': request.POST.get('shipping_province'),
            'shipping_code': request.POST.get('shipping_code'),
            'shipping_country': request.POST.get('shipping_country'),
        }
        request.session['my_shipping'] = my_shipping

        # Redirect to the checkout session for payment
        return redirect('checkout_session')

    return render(request, "payment/billing.html", {
        "cart_products": cart.get_prods(),
        "quantity": cart.get_quant(),
        "totals": cart.total()
    })


  
def pay_now(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': 'price_1QPN2DH4vnThRK4xRy2XllX0',  # Replace with actual Price ID from Stripe
                        'quantity': 2,
                    },
                ],
                mode='payment',
                success_url=settings.REDIRECT_DOMAIN + '/payment/payment_successful?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.REDIRECT_DOMAIN + '/payment_cancelled',
            )
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}", status=500)


def payment_successful(request):
    try:
        checkout_session_id = request.GET.get('session_id')
        if not checkout_session_id:
            return HttpResponse("Session ID is missing", status=400)

        # Retrieve session from Stripe (or payment service)
        session = stripe.checkout.Session.retrieve(checkout_session_id)
        customer_email = session.get('customer_email', 'Unknown')

        # Save payment details
        user_payment, created = userPayment.objects.get_or_create(app_user=request.user)
        user_payment.stripe_checkout_id = checkout_session_id
        user_payment.payment_bool = True
        user_payment.save()

        # Process the order after successful payment
        process_order(request)  # Call process_order

        return render(request, 'payment/payment_successful.html', {'customer_email': customer_email})

    except userPayment.DoesNotExist:
        return HttpResponse("User payment record not found", status=404)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)

def process_order(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    prod_quant = cart.get_quant()
    totals = cart.total()

    # Retrieve shipping session
    my_shipping = request.session.get('my_shipping')

    if not my_shipping:
        return HttpResponse("Shipping details are missing", status=400)

    if request.user.is_authenticated:
        user = request.user
        full_name = my_shipping['shipping_fullname']
        email = my_shipping['shipping_email']
        amount_paid = totals
        full_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_province']}\n{my_shipping['shipping_code']}\n{my_shipping['shipping_country']}"

        # Create order
        create_order = Order(
            user=user,
            full_name=full_name,
            email=email,
            shipping_Address=full_address,
            amount_paid=amount_paid,
        )
        create_order.save()

        order_id = create_order.pk

        # Loop through cart products and create order items
        for product in cart_products:
            product_id = product.id
            price = product.sale_price if product.is_sale else product.price
            quantity = prod_quant.get(str(product_id), 0)

            create_order_item = OrderItem(
                order_id=order_id,
                product_id=product_id,
                user=user,
                quantity=quantity,
                price=price,
            )
            create_order_item.save()

      # Clear the cart

    return redirect('index')


 
 

def payment_cancelled(request):
    return render(request, "payment/payment_cancelled.html")


def stripe_webhook(request):
    payload = request.body
    signature_header = request.META.get('HTTP_STRIPE_SIGNATURE', None)
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse("Invalid payload", status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse("Invalid signature", status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        session_id = session.get('id', None)

        try:
            user_payment = userPayment.objects.get(stripe_checkout_id=session_id)
            line_items = stripe.checkout.Session.list_line_items(session_id, limit=1)
            user_payment.payment_bool = True
            user_payment.save()
        except userPayment.DoesNotExist:
            return HttpResponse("User payment record not found", status=404)

    return HttpResponse(status=200)

import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from cart.cart import Cart  # Import your cart class

# Set up Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def create_checkout_session(request):
    cart = Cart(request)  # Access the cart
    cart_products = cart.get_prods
    prod_quant = cart.get_quant
    totals = cart.total

    line_items = []

    # Dynamically generate line items from the cart
    for product in cart.get_prods():
        item = {
            'price_data': {
                'currency': 'zar',
                'product_data': {
                    'name': product.name,  # Dynamically set product name
                },
                'unit_amount': int(product.price * 100),  # Stripe expects amounts in cents
            },
            'quantity': cart.get_quant().get(str(product.id)),  # Get product quantity
        }
        line_items.append(item)

    # Create a Stripe Checkout session
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
    success_url=settings.REDIRECT_DOMAIN + '/payment/payment_successful?session_id={CHECKOUT_SESSION_ID}',
    cancel_url=settings.REDIRECT_DOMAIN + '/payment_cancelled',# Redirect on cancel
    )

    # Redirect the user to the Stripe checkout session
    return redirect(session.url)
