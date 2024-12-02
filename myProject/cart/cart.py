from myApp.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session
        
        # get current session key if it exists
        cart = self.session.get('session_key')

        # Initialize cart in the session if it doesn't exist
        if 'session_key' not in self.session:
            cart = self.session['session_key'] = {}

        # Make sure cart 
        self.cart = cart
        

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = quantity
        # Add the product to the cart if not already present
        if product_id in self.cart:
           pass
        else:
            # Optionally update quantity, or handle an existing product logic here
            self.cart[product_id] = int(product_qty) # For example purposes

        # Update the session directly to ensure persistence
        # self.session['session_key'] = 'Hello World'
        self.session.modified = True
    
    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids )

        return products

    def get_quant(self):
        quan = self.cart
        return quan
    
    def update(self, product, quantity):
        try:
            product_id = str(product)
            product_qty = int(quantity)

            self.cart[product_id] = product_qty
            self.session.modified = True
            return self.cart
        except (ValueError, KeyError):
            raise ValueError('Invalid product or quantity')
        
    def delete(self, product):
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

    def total(self ):
        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids)
        quant = self.cart

        total = 0

        for key, value in quant.items():
            key = int(key)

            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value )
                    else:
                        total = total + (product.price * value )
        
        return total
