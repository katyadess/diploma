from shop.models import *
from shop.forms import *
from .models import *
from .forms import *
from cart.cart import Cart
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()

# Create your views here.

class CreateOrderView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/order.html'