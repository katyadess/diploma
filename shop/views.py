from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.views import View
from django.views.generic import ListView
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.db.models import Q

# Create your views here.

class MainPageView(View):
    
    def post(self, request):
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
        
        return redirect('shop:main')
    
    def get(self, request):   
        subscribe_form = SubscribeForm()
        brands = Brand.objects.all()
        categories = Category.objects.all()
        new_arrivals = Product.objects.all().order_by('-created_at')[:5]
        context = {'categories': categories, 'brands': brands, 'new_arrivals': new_arrivals, 'subscribe_form': subscribe_form}
        return render(request, 'shop/main.html', context)

class ProductListView(View):
    
    def post(self, request, category_slug=None):
        if category_slug: 
            category = get_object_or_404(Category, slug=category_slug)
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
        return redirect(f'{request.path}')
        
    
    def get(self, request, category_slug=None):
        
        
        subscribe_form = SubscribeForm()
        
        brands = Brand.objects.all()
        categories = Category.objects.all()
        
        if category_slug: 
            category = get_object_or_404(Category, slug=category_slug)
            subcategories = category.subcategories.all()
            subsubcategories_total = []
            for subcategory in subcategories:
                subsubcategories_total.extend(subcategory.subcategories.all())
            categories_to_include = category.get
        
        
        products = Product.objects.filter(category__name__in=categories_to_include)
        
        sort_by_value = request.GET.get('selected_value', '1')
        if sort_by_value == '2':
            products = products.order_by('price')
        elif sort_by_value == '3':
            products = products.order_by('-price')
        else:
            products = products.order_by('-created_at')
            
        
        # products = Product.objects.filter(category=category)
        
        breadcrumbs = [{'name': 'Main', 'url': reverse('shop:main')}]
        for parent in category.get_full_breadcrumb_path():
            breadcrumbs.append({'name': parent.name, 'url': parent.get_absolute_url()})
        breadcrumbs.append({'name': category.name, 'url': category.get_absolute_url(), 'class': 'active'})
            
        context = {
            'category': category,
            'breadcrumbs': breadcrumbs,
            'products': products,
            'categories':categories,
            'brands': brands,
            'subscribe_form': subscribe_form
        }
        
        return render(request, 'shop/product_list.html', context)
    
class SearchView(ListView):
    
    model = Product
    template_name = 'shop/search_results.html'
    paginate_by = 30
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query', '')
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        context['subscribe_form'] = SubscribeForm()
        return context
      
    def get_queryset(self):
        query = self.request.GET.get('query', '')
        return Product.objects.filter(Q(name__icontains=query) | Q(brief_description__icontains=query) | Q(brand__name__icontains=query))
         
    
    def post(self, request):
        query = self.request.GET.get('query', '')
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
        
        return redirect(f'{request.path}?query={query}')