from django.shortcuts import render
from django.views import View
from .models import *

# Create your views here.

class MainPageView(View):
    def get(self, request):
        
        brands = Brand.objects.all()
        categories = Category.objects.all()
        context = {'categories': categories, 'brands': brands}
        return render (request, 'shop/main.html', context)

# class ProductListView()