from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import ListView
from .models import *

# Create your views here.

class MainPageView(View):
    def get(self, request):
        
        brands = Brand.objects.all()
        categories = Category.objects.all()
        new_arrivals = Product.objects.all().order_by('-created_at')[:5]
        
        context = {'categories': categories, 'brands': brands, 'new_arrivals': new_arrivals}
        return render (request, 'shop/main.html', context)

class ProductListView(ListView):
    model = Product