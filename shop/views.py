from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from .models import *

# Create your views here.

class MainPageView(View):
    def get(self, request):
        
        brands = Brand.objects.all()
        categories = Category.objects.all()
        products = Product.objects.all()
        
        categorized_products = {}
        for category in categories:
            categorized_products[category] = Product.objects.filter(category=category)

        context = {'categories': categories, 'brands': brands, 'products': products, 'categorized_products': categorized_products}
        return render (request, 'shop/main.html', context)

class ProductListView(ListView):
    model = Product