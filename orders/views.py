from shop.models import *
from shop.forms import *
from .models import *
from .forms import *
from cart.cart import Cart
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()

# Create your views here.

class CreateOrderView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/order.html'
    
    def dispatch(self, request, *args, **kwargs):
        cart = Cart(self.request)
        if len(cart) == 0:
            return redirect(reverse_lazy('shop:main'))
        return super().dispatch(request, *args, **kwargs)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        context['subscribe_form'] = SubscribeForm()
        
        cart = Cart(self.request)
        context['cart'] = cart
        
        out_of_stock = False
        invalid_quantity = False
        
        for item in cart:
            if item['product'].stock == 0:
                out_of_stock = True
                
            if item['quantity'] > item['product'].stock:
                invalid_quantity = True
        
        context['out_of_stock'] = out_of_stock
        context['invalid_quantity'] = invalid_quantity
        context['order_form'] = OrderForm(user=self.request.user)
        
        return context
    
    def post(self, request):
        
        if 'subscribe' in request.POST:
            subscribe_form = SubscribeForm(request.POST)
            if subscribe_form.is_valid():
                subscribe_form.send_email()
                subscribe_form.save()
                messages.success(request, "You have successfully subscribed to our newsletter!")
            else:
                messages.info(request, "Invalid email or you had already subscribed to our newsletter.")
        
        elif 'toggle-cart' in request.POST:
            product_id = request.POST.get('product_id')
            product = Product.objects.get(id=product_id)
            cart = Cart(self.request)
            if product in cart:
                cart.remove(product)
                if len(cart) == 0:
                    return redirect('shop:main')
            else:
                cart.add(product)
        
        elif 'create-order' in request.POST:
            
            cart = Cart(self.request)
            order_form = OrderForm(self.request.POST, user=self.request.user)
            if order_form.is_valid() and order_form.cleaned_data.get('address'):
                
                address = order_form.cleaned_data.get('address')
                order_form.instance.address = address
                order = order_form.save()
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        quantity=item['quantity']
                    )
                    product = item['product']
                    product.stock -= item['quantity']
                    product.save()  
                
                    cart.clear()
                    messages.success(request, "Your order was successfully submited!")
                    return HttpResponseRedirect(f'{reverse('shop:account')}?show=orders')
            
            elif not order_form.is_valid() and not order_form.cleaned_data.get('address'):
                
                first_name = request.POST.get('first-name')
                last_name = request.POST.get('last-name')
                street = request.POST.get('street')
                city = request.POST.get('city')
                phone_number = request.POST.get('phone-number')
                
                address = Address.objects.create(
                    user=request.user,
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number,
                    city=city,
                    street=street
                )
            
                order_form.instance.address = address
                
                if order_form.is_valid():
                
                    order = order_form.save()
                    for item in cart:
                        OrderItem.objects.create(
                            order=order,
                            product=item['product'],
                            price=item['price'],
                            quantity=item['quantity']
                        )
                        product = item['product']
                        product.stock -= item['quantity']
                        product.save()  
                    
                    cart.clear()
                    messages.success(request, "Your order was successfully submited!")
                    return HttpResponseRedirect(f'{reverse('shop:account')}?show=orders')
            else: 
                              
                messages.error(request, "Invalid form")
                
        else:
            
            product_id = request.POST.get('product_id')
            try:
                quantity = int(request.POST.get('quantity'))
            except ValueError:
                return redirect('orders:order')
            product = Product.objects.get(id=product_id)
            cart = Cart(self.request)
            if quantity > 0:
                cart.add(product=product, quantity=quantity, update_quantity=True)
                
        
        return redirect('orders:order')

    