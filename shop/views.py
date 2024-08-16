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
        return render(request, 'shop/main.html', context)

class ProductListView(View):
    
    def get(self, request, category_slug=None):
        
        if category_slug: 
            category = get_object_or_404(Category, slug=category_slug)
        
        products = Product.objects.filter(category=category)
        
        breadcrumbs = [{'name': 'Main', 'url': reverse('shop:main')}]
        for parent in category.get_full_breadcrumb_path():
            breadcrumbs.append({'name': parent.name, 'url': parent.get_absolute_url()})
        breadcrumbs.append({'name': category.name, 'url': category.get_absolute_url(), 'class': 'active'})
            
        context = {
            'category': category,
            'breadcrumbs': breadcrumbs,
            'products': products
        }
        
        return render(request, 'shop/product_list.html', context)