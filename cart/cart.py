from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        current_price = str(product.price_new) if product.price_new else str(product.price)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(current_price)}
        
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
         
        stock_quantity = product.stock
        current_quantity = self.cart[product_id]['quantity']
        if current_quantity > stock_quantity:
            self.cart[product_id]['quantity'] = stock_quantity 
               
        self.save()
        
    
    def save(self):
        
        for item in self.cart.values():
            item['price'] = str(item['price'])
        
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
        
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
            
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            
            self.cart[str(product.id)]['product'] = product
            self.cart[str(product.id)]['price'] = str(product.price_new) if product.price_new else str(product.price)
    
            
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    
    def __contains__(self, product):
        
        return str(product.id) in self.cart
    
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_quantity(self, product_id):
        return self.cart.get(product_id, {}).get('quantity', 0)

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True