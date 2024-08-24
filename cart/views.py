from shop.models import *
from shop.forms import *
from .forms import *
from .cart import *
from django.db.models import F, Avg
from django.contrib import messages
from django.utils import timezone
from django.db.models.functions import Coalesce
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, TemplateView, FormView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()

# Create your views here.


class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'cart/cart.html'
    
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
            else:
                cart.add(product)
        
        return redirect('cart:cart')

    
    