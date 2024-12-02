from django.shortcuts import render, get_object_or_404
from .cart import Cart
from myApp.models import Product
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    prod_quant = cart.get_quant

    totals = cart.total()
    return render(request, "cart/cart_summary.html", {"cart_products": cart_products, "quantity": prod_quant, "totals": totals })


def cart_add(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_qty = request.POST.get('product_qty')
        if not product_id:
            return JsonResponse({'message': 'No product ID provided'}, status=400)
        
        try:
            # Convert product_id to integer and get product
            product = get_object_or_404(Product, id=int(product_id))
        except ValueError:
            return JsonResponse({'message': 'Invalid product ID format'}, status=400)
    
        cart.add(product=product, quantity=product_qty )
      
        cart_quantity = cart.__len__()
         # Return JSON response
        messages.success(request, ("Product added to cart..... "))
        return JsonResponse({'qty': cart_quantity})

       
def cart_delete(request):
    cart = Cart(request)

    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))

        cart.delete(product=product_id) 
        messages.success(request, ("Item removed from your cart..... "))   
        return JsonResponse({'ID': product_id })


def cart_update(request):
    cart = Cart(request)

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_qty = request.POST.get('product_qty')

        if not product_id or not product_qty:
            return JsonResponse({'error': 'Invalid data'}, status=400)

        try:
            cart = Cart(request)
            cart.update(product=product_id, quantity=product_qty)
            messages.success(request, ("Item removed from your cart..... ")) 
            return JsonResponse({'qty': product_qty})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
             
    return JsonResponse({'error': 'Invalid request method'}, status=405)



