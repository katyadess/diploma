from django.db.models import F
from django.utils import timezone
from django.db.models.functions import Coalesce
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, TemplateView
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator

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
        categories = Category.objects.filter(parent__isnull=True)
        
        now = timezone.now()
        
        new_arrivals = Product.objects.filter(
            created_at__month=now.month
        ).order_by('-created_at')[:5]
        
        category_products = {}
        for category in categories:
            descendants = category.get_descendants()
            products = Product.objects.filter(category__in=descendants)
            category_products[category] = products
            
        context = {
            'categories': categories, 
            'brands': brands, 
            'new_arrivals': new_arrivals, 
            'subscribe_form': subscribe_form,
            'category_products': category_products
            }
        return render(request, 'shop/main.html', context)

class ProductListView(View):
    
    def post(self, request, category_slug=None):
        if category_slug: 
            category = get_object_or_404(Category, slug=category_slug)
        
        sort_by_value = self.request.GET.get('sort_by')
        price_min = self.request.GET.get('min_price')
        price_max = self.request.GET.get('max_price')
        page = self.request.GET.get('page')
        
        redirect_url = f'{request.path}?'
        
        if sort_by_value:
            redirect_url += f'sort_by={sort_by_value}&'
            
        if price_min or price_max:
            redirect_url += f'min_price={price_min}&max_price={price_max}&'
        
        if page:
            redirect_url += f'page={page}&'
        
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
    
        return redirect(redirect_url)
        
    
    def get(self, request, category_slug=None):
        
        
        subscribe_form = SubscribeForm()
        
        brands = Brand.objects.all()
        categories = Category.objects.all()
        
        if category_slug: 
            category = get_object_or_404(Category, slug=category_slug)
            all_categories = category.get_descendants(include_self=True)
            
        price_min = self.request.GET.get('min_price', '3')
        price_max = self.request.GET.get('max_price', '1000')
        
        
        products = Product.objects.annotate(current_price=Coalesce('price_new', F('price'))
                ).filter(category__in=all_categories)
        
        products = products.filter(current_price__gte=price_min, current_price__lte=price_max)
        
        
        sort_by_value = self.request.GET.get('sort_by', 'default')
        if sort_by_value == 'lowest_price':
            products = products.order_by('current_price')
        elif sort_by_value == 'highest_price':
            products = products.order_by('-current_price')
        else:
            products = products.order_by('-created_at')

        paginator = Paginator(products, 4)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        breadcrumbs = [{'name': 'Main', 'url': reverse('shop:main')}]
        for parent in category.get_full_breadcrumb_path():
            breadcrumbs.append({'name': parent.name, 'url': parent.get_absolute_url()})
        breadcrumbs.append({'name': category.name, 'url': category.get_absolute_url(), 'class': 'active'})
            
        context = {
            'category': category,
            'breadcrumbs': breadcrumbs,
            'categories':categories,
            'brands': brands,
            'subscribe_form': subscribe_form,
            'page_obj': page_obj,
        }
        
        return render(request, 'shop/product_list.html', context)

class NewArrivalsView(View):
    
    def post(self, request):
        
        sort_by_value = self.request.GET.get('sort_by')
        price_min = self.request.GET.get('min_price')
        price_max = self.request.GET.get('max_price')
        page = self.request.GET.get('page')
        
        redirect_url = f'{request.path}?'
        
        if sort_by_value:
            redirect_url += f'sort_by={sort_by_value}&'
            
        if price_min or price_max:
            redirect_url += f'min_price={price_min}&max_price={price_max}&'
        
        if page:
            redirect_url += f'page={page}&'
        
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
    
        return redirect(redirect_url)
        
    
    def get(self, request):
        
        
        subscribe_form = SubscribeForm()
        
        brands = Brand.objects.all()
        categories = Category.objects.all()
        
            
        price_min = self.request.GET.get('min_price', '3')
        price_max = self.request.GET.get('max_price', '1000')
        
        
        now = timezone.now()
        
        products = Product.objects.annotate(
            current_price=Coalesce('price_new', F('price'))
        ).filter(created_at__month=now.month
        ).order_by('-created_at')
        
        products = products.filter(current_price__gte=price_min, current_price__lte=price_max)
        
        
        sort_by_value = self.request.GET.get('sort_by', 'default')
        if sort_by_value == 'lowest_price':
            products = products.order_by('current_price', '-created_at')
        elif sort_by_value == 'highest_price':
            products = products.order_by('-current_price', '-created_at')
        else:
            products = products.order_by('-created_at')

        paginator = Paginator(products, 4)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
            
        context = {
            'categories':categories,
            'brands': brands,
            'subscribe_form': subscribe_form,
            'page_obj': page_obj,
        }
        
        return render(request, 'shop/new_arrivals.html', context)
  

class SearchView(ListView):
    
    model = Product
    paginate_by = 4
    template_name = 'shop/search_results.html'
    
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query', '')
        context['sort_by'] = self.request.GET.get('sort_by', 'default')
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        context['subscribe_form'] = SubscribeForm()
        context['price_min'] = self.request.GET.get('min_price', '3')
        context['price_max'] = self.request.GET.get('max_price', '1000')
        
        full_query_length = self.get_queryset().count()
        context['full_query_length'] = full_query_length
        
        return context
  
    def get_queryset(self):
    
        query = self.request.GET.get('query', '')
        sort_by_value = self.request.GET.get('sort_by', 'default')
        price_min = self.request.GET.get('min_price', '3')
        price_max = self.request.GET.get('max_price', '1000')
        

        products = Product.objects.annotate(
            current_price=Coalesce('price_new', F('price'))
            ).filter(
            Q(name__icontains=query) | 
            Q(brief_description__icontains=query) | 
            Q(brand__name__icontains=query))
        
        products = products.filter(current_price__gte=price_min, current_price__lte=price_max)
        
        if sort_by_value == 'lowest_price':
            products = products.order_by('current_price')
        elif sort_by_value == 'highest_price':
            products = products.order_by('-current_price')
        else:
            products = products.order_by('-created_at')
            
        return products 
    
    
    def post(self, request):
        
        
        query = self.request.GET.get('query')
        sort_by_value = self.request.GET.get('sort_by')
        price_min = self.request.GET.get('min_price')
        price_max = self.request.GET.get('max_price')
        page = self.request.GET.get('page')
        
        redirect_url = f'{request.path}?query={query}'
        
        if sort_by_value:
            redirect_url += f'&sort_by={sort_by_value}'
            
        if price_min or price_max:
            redirect_url += f'&min_price={price_min}&max_price={price_max}'
        
        if page:
            redirect_url += f'&page={page}'
        
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
    
        return redirect(redirect_url)
    
class BrandsView(View):
    
    def get(self, request):
        
        subscribe_form = SubscribeForm()
        categories = Category.objects.all()
        brands = Brand.objects.all()
        category_brands = brands.all()
        sort_by_value = self.request.GET.get('sort_by', 'all')
        
        sorting_values = ['makeup', 'face-care', 'hair-care', 'body-care']
        
        for value in sorting_values:
            if sort_by_value == value:
                value_category = get_object_or_404(Category, slug=value)
                all_subcategories = value_category.get_descendants(include_self=True)
                category_brands = category_brands.filter(brand_products__category__in=all_subcategories)        
        
        context = {
            'categories':categories,
            'brands': brands,
            'category_brands': category_brands,
            'subscribe_form': subscribe_form
        }
        
        return render(request, 'shop/brands.html', context)
    
    def post(self, request, brand_slug=None):
        if brand_slug: 
            brand = get_object_or_404(Brand, slug=brand_slug)
        
        sort_by_value = self.request.GET.get('sort_by')
        redirect_url = f'{request.path}?'
        
        if sort_by_value:
            redirect_url += f'sort_by={sort_by_value}'
            
        
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
    
        return redirect(redirect_url)
    
    
class BrandsProductView(View):
    
    def post(self, request, brand_slug=None):
        
        if brand_slug: 
            brand = get_object_or_404(Brand, slug=brand_slug)
        
        sort_by_value = self.request.GET.get('sort_by')
        price_min = self.request.GET.get('min_price')
        price_max = self.request.GET.get('max_price')
        
        redirect_url = f'{request.path}?'
        
        if sort_by_value:
            redirect_url += f'sort_by={sort_by_value}&'
            
        if price_min or price_max:
            redirect_url += f'min_price={price_min}&max_price={price_max}&'
        
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
    
        return redirect(redirect_url)
        
    
    def get(self, request, brand_slug=None):
        
        
        subscribe_form = SubscribeForm()
        
        brands = Brand.objects.all()
        
        if brand_slug: 
            brand = get_object_or_404(Brand, slug=brand_slug)
            
        price_min = request.GET.get('min_price', '3')
        price_max = request.GET.get('max_price', '1000')
        
        
        products = Product.objects.annotate(current_price=Coalesce('price_new', F('price'))
                ).filter(brand=brand)
        
        products = products.filter(current_price__gte=price_min, current_price__lte=price_max)
        
        sort_by_value = self.request.GET.get('sort_by', 'default')
        if sort_by_value == 'lowest_price':
            products = products.order_by('current_price')
        elif sort_by_value == 'highest_price':
            products = products.order_by('-current_price')
        else:
            products = products.order_by('-created_at')
            
        paginator = Paginator(products, 4)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        
        breadcrumbs = [{'name': 'Main', 'url': reverse('shop:main')}, 
                       {'name': 'Brands', 'url': reverse('shop:product_brands')},
                       {'name': brand.name, 'url': brand.get_absolute_url(), 'class': 'active'}]
        
            
        context = {
            'breadcrumbs': breadcrumbs,
            'page_obj': page_obj,
            'brands': brands,
            'brand': brand,
            'subscribe_form': subscribe_form
        }
        
        return render(request, 'shop/brands_product_list.html', context)
    
    
class HelpView(TemplateView):
    template_name = 'shop/q-a.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        context['subscribe_form'] = SubscribeForm()
        
        return context
    
    def post(self, request):
        
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
        
        return redirect('shop:help')
