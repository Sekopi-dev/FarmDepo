from .cart import Cart

# Create Context processor so our cart can work on all pages 
def cart(request):
    return {'cart': Cart(request)}



