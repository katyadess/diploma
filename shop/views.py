from django.db.models import F, Avg, Q
from django.contrib import messages
from datetime import timedelta
from .tasks import *
from cart.forms import *
from cart.cart import Cart
from orders.models import *
from django.utils import timezone
from django.db.models.functions import Coalesce
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, TemplateView, FormView, DetailView
from django.contrib.auth.views import LoginView, PasswordChangeView
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()



class MainPageView(View):
    
    def post(self, request):
        
        if 'subscribe' in request.POST:
            subscribe_form = SubscribeForm(request.POST)
            if subscribe_form.is_valid():
                subscribe_form.send_email()
                subscribe_form.save()
                messages.success(request, "You have successfully subscribed to our newsletter!")
            else:
                messages.info(request, "Invalid email or you had already subscribed to our newsletter.")
                       
                
        
        elif 'toggle_wishlist' in request.POST:
            product_id = request.POST.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            wishlist, created = WishList.objects.get_or_create(user=request.user)
            if product in wishlist.products.all():
                wishlist.products.remove(product)
            else:
                wishlist.products.add(product) 
        
        elif 'toggle-cart' in request.POST:
            product_id = request.POST.get('product_id')
            product = Product.objects.get(id=product_id)
            cart = Cart(self.request)
            if product in cart:
                cart.remove(product)
            else:
                cart.add(product, update_quantity=True)
            
        return redirect('shop:main')
    
    def get(self, request):   
        cart = Cart(request)
        subscribe_form = SubscribeForm()
        brands = Brand.objects.all()
        categories = Category.objects.filter(parent__isnull=True)
        
        
        new_arrivals = Product.objects.filter(     
            stock__gt=0,
            is_available=True
        ).annotate(
            average_rating=Avg('reviews__rating')
        ).order_by('-created_at')[:10]
        
        discount_products = Product.objects.filter(
            stock__gt=0,
            is_available=True,
            price_new__isnull=False
        )[:10]
        
        category_products = {}
        for category in categories:
            descendants = category.get_descendants()
            products = Product.objects.filter(
                category__in=descendants,
                stock__gt=0
            ).annotate(
                average_rating=Avg('reviews__rating')
            )[:20]
            category_products[category] = products
            
        context = {
            'categories': categories, 
            'brands': brands, 
            'new_arrivals': new_arrivals, 
            'discount_products': discount_products,
            'subscribe_form': subscribe_form,
            'category_products': category_products,
            'cart': cart
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
        
        if 'subscribe' in request.POST:
        
            subscribe_form = SubscribeForm(request.POST)
            if subscribe_form.is_valid():
                subscribe_form.send_email()
                subscribe_form.save()
                messages.success(request, "You have successfully subscribed to our newsletter!")
            else:
                messages.info(request, "Invalid email or you had already subscribed to our newsletter.")
        
        
        elif 'toggle_wishlist' in request.POST:
            product_id = request.POST.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            wishlist, created = WishList.objects.get_or_create(user=request.user)
            if product in wishlist.products.all():
                wishlist.products.remove(product)
            else:
                wishlist.products.add(product)
                
        elif 'toggle-cart' in request.POST:
            product_id = request.POST.get('product_id')
            product = Product.objects.get(id=product_id)
            cart = Cart(self.request)
            if product in cart:
                cart.remove(product)
            else:
                cart.add(product, update_quantity=True)
    
        return redirect(redirect_url)
        
    
    def get(self, request, category_slug=None):
        
        cart = Cart(request)
        
        subscribe_form = SubscribeForm()
        
        brands = Brand.objects.all()
        categories = Category.objects.all()
        
        if category_slug: 
            category = get_object_or_404(Category, slug=category_slug)
            all_categories = category.get_descendants(include_self=True)
            
        price_min = self.request.GET.get('min_price', '3')
        price_max = self.request.GET.get('max_price', '1000')
        
        
        
        products = Product.objects.annotate(
            current_price=Coalesce('price_new', F('price')), 
            average_rating=Avg('reviews__rating')
            ).filter(
                category__in=all_categories,
                stock__gt=0,
                is_available=True
            )
        
        products = products.filter(
            current_price__gte=price_min, 
            current_price__lte=price_max
        )
        
        
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
            'cart': cart,
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
        
        if 'subscribe' in request.POST:
            
            subscribe_form = SubscribeForm(request.POST)
            if subscribe_form.is_valid():
                subscribe_form.send_email()
                subscribe_form.save()
                messages.success(request, "You have successfully subscribed to our newsletter!")
            else:
                messages.info(request, "Invalid email or you had already subscribed to our newsletter.")
        
        
        if 'toggle_wishlist' in request.POST:
            product_id = request.POST.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            wishlist, created = WishList.objects.get_or_create(user=request.user)
            if product in wishlist.products.all():
                wishlist.products.remove(product)
            else:
                wishlist.products.add(product)
        
        elif 'toggle-cart' in request.POST:
            product_id = request.POST.get('product_id')
            product = Product.objects.get(id=product_id)
            cart = Cart(self.request)
            if product in cart:
                cart.remove(product)
            else:
                cart.add(product, update_quantity=True)
            
        return redirect(redirect_url)
        
    
    def get(self, request):
        
        cart = Cart(request)
        
        subscribe_form = SubscribeForm()
        
        brands = Brand.objects.all()
        categories = Category.objects.all()
        
            
        price_min = self.request.GET.get('min_price', '3')
        price_max = self.request.GET.get('max_price', '1000')
        
        
        now = timezone.now()
        time_range = now - timedelta(days=90)
        
        products = Product.objects.annotate(
            current_price=Coalesce('price_new', F('price')),
            average_rating=Avg('reviews__rating')
        ).filter(
            created_at__gte=time_range,
            stock__gt=0,
            is_available=True
        ).order_by('-created_at')
        
        products = products.filter(
            current_price__gte=price_min, 
            current_price__lte=price_max
        )
        
        
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
            'cart': cart
        }
        
        return render(request, 'shop/new_arrivals.html', context)
 
 
class DiscountProductsView(View):
    
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
        
        if 'subscribe' in request.POST:
            
            subscribe_form = SubscribeForm(request.POST)
            if subscribe_form.is_valid():
                subscribe_form.send_email()
                subscribe_form.save()
                messages.success(request, "You have successfully subscribed to our newsletter!")
            else:
                messages.info(request, "Invalid email or you had already subscribed to our newsletter.")
        
        
        if 'toggle_wishlist' in request.POST:
            product_id = request.POST.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            wishlist, created = WishList.objects.get_or_create(user=request.user)
            if product in wishlist.products.all():
                wishlist.products.remove(product)
            else:
                wishlist.products.add(product)
        
        elif 'toggle-cart' in request.POST:
            product_id = request.POST.get('product_id')
            product = Product.objects.get(id=product_id)
            cart = Cart(self.request)
            if product in cart:
                cart.remove(product)
            else:
                cart.add(product, update_quantity=True)
            
        return redirect(redirect_url)
        
    
    def get(self, request):
        
        cart = Cart(request)
        
        subscribe_form = SubscribeForm()
        
        brands = Brand.objects.all()
        categories = Category.objects.all()
        
            
        price_min = self.request.GET.get('min_price', '3')
        price_max = self.request.GET.get('max_price', '1000')
        
        
        products = Product.objects.annotate(
            current_price=Coalesce('price_new', F('price')),
            average_rating=Avg('reviews__rating')
        ).filter(
            price_new__isnull=False,
            stock__gt=0,
            is_available=True
        ).order_by('-created_at')
        
        products = products.filter(
            current_price__gte=price_min, 
            current_price__lte=price_max
        )
        
        
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
            'cart': cart
        }
        
        return render(request, 'shop/discount_products.html', context)
 
 

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
        
        cart = Cart(self.request)
        context['cart'] = cart
        
        return context
  
    def get_queryset(self):
    
        query = self.request.GET.get('query', '')
        sort_by_value = self.request.GET.get('sort_by', 'default')
        price_min = self.request.GET.get('min_price', '3')
        price_max = self.request.GET.get('max_price', '1000')
        

        products = Product.objects.annotate(
            current_price=Coalesce('price_new', F('price')),
            average_rating=Avg('reviews__rating')
            ).filter(
            Q(name__icontains=query) | 
            Q(brief_description__icontains=query) | 
            Q(brand__name__icontains=query),
            stock__gt=0,
            is_available=True
        )
        
        products = products.filter(
            current_price__gte=price_min, 
            current_price__lte=price_max
        )
        
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
        
        if 'subscribe' in request.POST:
            
            subscribe_form = SubscribeForm(request.POST)
            if subscribe_form.is_valid():
                subscribe_form.send_email()
                subscribe_form.save()
                messages.success(request, "You have successfully subscribed to our newsletter!")
            else:
                messages.info(request, "Invalid email or you had already subscribed to our newsletter.")
        
        
        elif 'toggle_wishlist' in request.POST:
            product_id = request.POST.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            wishlist, created = WishList.objects.get_or_create(user=request.user)
            if product in wishlist.products.all():
                wishlist.products.remove(product)
            else:
                wishlist.products.add(product)
                
        elif 'toggle-cart' in request.POST:
            product_id = request.POST.get('product_id')
            product = Product.objects.get(id=product_id)
            cart = Cart(self.request)
            if product in cart:
                cart.remove(product)
            else:
                cart.add(product, update_quantity=True)
    
        return redirect(redirect_url)
    
class BrandsView(View):
    
    def get(self, request):
        cart = Cart(request)
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
            'subscribe_form': subscribe_form,
            'cart': cart
        }
        
        return render(request, 'shop/brands.html', context)
    
    def post(self, request, brand_slug=None):
        if brand_slug: 
            brand = get_object_or_404(Brand, slug=brand_slug)
        
        sort_by_value = self.request.GET.get('sort_by')
        redirect_url = f'{request.path}?'
        
        if sort_by_value:
            redirect_url += f'sort_by={sort_by_value}'
            
        
        if 'subscribe' in request.POST:
            subscribe_form = SubscribeForm(request.POST)
            if subscribe_form.is_valid():
                subscribe_form.send_email()
                subscribe_form.save()
                messages.success(request, "You have successfully subscribed to our newsletter!")
            else:
                messages.info(request, "Invalid email or you had already subscribed to our newsletter.")
        
    
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
        
        if 'subscribe' in request.POST:
            
            subscribe_form = SubscribeForm(request.POST)
            if subscribe_form.is_valid():
                subscribe_form.send_email()
                subscribe_form.save()
                messages.success(request, "You have successfully subscribed to our newsletter!")
            else:
                messages.info(request, "Invalid email or you had already subscribed to our newsletter.")
        
        
        if 'toggle_wishlist' in request.POST:
            product_id = request.POST.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            wishlist, created = WishList.objects.get_or_create(user=request.user)
            if product in wishlist.products.all():
                wishlist.products.remove(product)
            else:
                wishlist.products.add(product)
                
        elif 'toggle-cart' in request.POST:
            product_id = request.POST.get('product_id')
            product = Product.objects.get(id=product_id)
            cart = Cart(self.request)
            if product in cart:
                cart.remove(product)
            else:
                cart.add(product, update_quantity=True)
            
    
        return redirect(redirect_url)
        
    
    def get(self, request, brand_slug=None):
        
        cart = Cart(request)
        
        subscribe_form = SubscribeForm()
        
        brands = Brand.objects.all()
        
        if brand_slug: 
            brand = get_object_or_404(Brand, slug=brand_slug)
            
        price_min = request.GET.get('min_price', '3')
        price_max = request.GET.get('max_price', '1000')
        
        
        products = Product.objects.annotate(
            current_price=Coalesce('price_new', F('price')),
            average_rating=Avg('reviews__rating')
            ).filter(
                brand=brand,
                stock__gt=0,
                is_available=True
            )
        
        products = products.filter(
            current_price__gte=price_min, 
            current_price__lte=price_max)
        
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
            'subscribe_form': subscribe_form,
            'cart': cart
        }
        
        return render(request, 'shop/brands_product_list.html', context)
    
    
class HelpView(TemplateView):
    template_name = 'shop/q-a.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        context['subscribe_form'] = SubscribeForm()
        cart = Cart(self.request)
        context['cart'] = cart
        
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
        
        
        return redirect('shop:help')

class ContactView(FormView):
    template_name = 'shop/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('shop:contact')
    
    def post(self, request, *args, **kwargs):
        
        if 'subscribe' in request.POST:
            subscribe_form = SubscribeForm(request.POST)
            if subscribe_form.is_valid():
                subscribe_form.send_email()
                subscribe_form.save()
                messages.success(request, "You have successfully subscribed to our newsletter!")
            else:
                messages.info(request, "Invalid email or you had already subscribed to our newsletter.")
        
                
            return redirect(self.success_url)
            
        else:
            contact_form = ContactForm(request.POST, request.FILES)
            if contact_form.is_valid():
                return self.form_valid(contact_form)
            else:
                return self.form_invalid(contact_form)
    
    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, "Your message was successfully sent! We will contact you as soon as we can.")
            
        return super().form_valid(form)
    
    def form_invalid(self, contact_form):
        context = self.get_context_data(form=contact_form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        context['subscribe_form'] = SubscribeForm()
        cart = Cart(self.request)
        context['cart'] = cart
        return context
    
    
@login_required
def account(request):
    user_data = get_object_or_404(UserData, user=request.user)  
    addresses = Address.objects.filter(user=request.user, is_archived=False)          
    
    
    address_edit_forms = {}
    for address in addresses:
        address_edit_forms[address] = EditAddressForm(instance=address)
    
    if request.method == 'POST':
        
        if 'subscribe' in request.POST:
            subscribe_form = SubscribeForm(request.POST)
            if subscribe_form.is_valid():
                subscribe_form.send_email()
                subscribe_form.save()
                messages.success(request, "You have successfully subscribed to our newsletter!")
            else:
                messages.info(request, "Invalid email or you had already subscribed to our newsletter.")

        
        elif 'account' in request.POST:
            edit_account_form = EditAccountForm(request.POST, instance=request.user)
            edit_phone_form = EditPhoneForm(request.POST, instance=user_data)
            
            if edit_account_form.is_valid() and edit_phone_form.is_valid():
                edit_account_form.save()
                phone = edit_phone_form.cleaned_data.get('telephone')
                user_data.telephone = phone
                user_data.save()
        
        elif 'save-address' in request.POST:
            add_address_form = AddAddressForm(request.POST)
            if add_address_form.is_valid():
                new_address = add_address_form.save(commit=False)
                new_address.user = request.user
                new_address.save()
                
                return redirect(f'{request.path}?show=addresses')
            
        elif 'edit-address' in request.POST:
            address_id = request.POST.get('address_id')
            address = get_object_or_404(Address, id=address_id, user=request.user)
            edit_address_form = EditAddressForm(request.POST, instance=address)
            if edit_address_form.is_valid():
                edit_address_form.save()
                
                return redirect(f'{request.path}?show=addresses')
            
        elif 'delete-address' in request.POST:
            address_id = request.POST.get('address_id')
            if address_id:
                address = get_object_or_404(Address, id=address_id, user=request.user)
                orders_with_address = Order.objects.filter(address=address)
                
                if orders_with_address.filter(status__in=[Order.SENT, Order.DELIVERED]).exists():
                    messages.error(request, "Cannot delete address because there are orders that have already been sent or delivered.")
                else:
                    orders_to_update = orders_with_address.exclude(
                        status__in=[
                            Order.SENT, 
                            Order.DELIVERED, 
                            Order.COMPLETED,
                            Order.CANCELED 
                        ]
                    )
                    
                    for order in orders_to_update:
                        order.status = Order.FAILED
                        order.save()
                        
                        for item in order.items.all():
                            product = item.product
                            product.stock += item.quantity
                            product.save()
                    
                    
                    address.is_archived = True
                    address.save()
                
                return redirect(f'{request.path}?show=addresses')
            
        elif 'toggle_wishlist' in request.POST:
            product_id = request.POST.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            wishlist, created = WishList.objects.get_or_create(user=request.user)
            if product in wishlist.products.all():
                wishlist.products.remove(product)
            else:
                wishlist.products.add(product)
            
            return redirect(f'{request.path}?show=favourites')
                
        elif 'toggle-cart' in request.POST:
            product_id = request.POST.get('product_id')
            product = Product.objects.get(id=product_id)
            cart = Cart(request)
            if product in cart:
                cart.remove(product)
            else:
                cart.add(product, update_quantity=True)
                
            return redirect(f'{request.path}?show=favourites')
        
        elif 'cancel-order' in request.POST:
            order_id = request.POST.get('order_id')
            order = Order.objects.get(id=order_id)
            
            if order.status != 'canceled':
                order_items = order.items.all()
                for item in order_items:
                    product = item.product
                    product.stock += item.quantity
                    product.save()
                    
            order.status = 'canceled'
            order.save()
            messages.success(request, "The order was canceled.")
            return redirect(f'{request.path}?show=orders')
        
        elif 'delete-acc' in request.POST:
            user_delete_form = UserDeleteForm(request.POST, instance=request.user)
            if user_delete_form.is_valid():
                
                user = request.user
                if not user.is_superuser and not user.is_staff:
                    # logout(request)
                    user.delete()
                else:
                    messages.warning(request, 'You cannot delete user this way')
            else:
                print('invalid')
            # return redirect('main')
            
        return redirect(f'{request.path}')
        
    categories = Category.objects.all()
    brands = Brand.objects.all()
    subscribe_form = SubscribeForm()
    edit_account_form = EditAccountForm(instance=request.user)
    edit_phone_form = EditPhoneForm(instance=user_data)
    add_address_form = AddAddressForm()
    wishlist, created = WishList.objects.get_or_create(user=request.user)
    wishlist_products = wishlist.products.annotate(
        average_rating=Avg('reviews__rating')
    )
    cart = Cart(request)
    orders = Order.objects.filter(user=request.user)
    user_delete_form = UserDeleteForm(instance=request.user)
    
    now = timezone.now()
    
    filter_orders = request.GET.get('filter_orders', 'all')
    if filter_orders == 'this-month':
        start_date = now.replace(day=1)
        orders = orders.filter(created__gte=start_date).order_by('-created')
    elif filter_orders == 'last-month':
        first_day_of_current_month = now.replace(day=1)
        last_month = first_day_of_current_month - timedelta(days=1)
        start_date = last_month.replace(day=1)
        end_date = first_day_of_current_month - timedelta(seconds=1)
        orders = orders.filter(created__gte=start_date, created__lte=end_date).order_by('-created')
    elif filter_orders == 'this-year':
        start_date = now.replace(month=1, day=1)
        orders = orders.filter(created__gte=start_date).order_by('-created')
    elif filter_orders == 'last-year': 
        first_day_of_current_year = now.replace(month=1, day=1)
        last_year = first_day_of_current_year - timedelta(days=1)
        start_date = last_year.replace(month=1, day=1)
        end_date = first_day_of_current_year - timedelta(seconds=1)
        orders = orders.filter(created__gte=start_date, created__lte=end_date).order_by('-created')
    else:
        orders = orders.order_by('-created')
    
    order_total_price = {}

    for order in orders:
        order_items = order.items.all()
        total_cost = sum(item.get_cost() for item in order_items)
        order_total_price[order] = total_cost

    
     
    context = {
        'categories': categories,
        'brands': brands,
        'subscribe_form': subscribe_form,
        'edit_account_form': edit_account_form,
        'edit_phone_form': edit_phone_form,
        'add_address_form': add_address_form,
        'addresses': addresses,
        'address_edit_forms': address_edit_forms,
        'wishlist_products': wishlist_products,
        'cart': cart,
        'orders': orders,
        'order_total_price': order_total_price,
        'user_delete_form': user_delete_form,
    }
    
    return render(request, 'shop/account.html', context)



class MyPasswordChangeView(PasswordChangeView):
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy('shop:account')
    form_class = PasswordChangeForm
    success_message = "Your password has been successfully changed!" 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        context['cart'] = Cart(self.request)
        return context
    
    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

    
class MyLogoutView(View):
     def get(self, request):
        logout(request)
        return redirect('shop:main')
        
      
class MyLoginView(LoginView):
    
    template_name = 'registration/login.html'
    success_url = reverse_lazy('shop:main')
    form_class = CustomLoginForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        context['cart'] = Cart(self.request)
        return context
    
    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)
    
    
class RegisterView(FormView):
    template_name = 'registration/register.html'
    success_url = reverse_lazy('shop:main')
    form_class = RegisterForm
    
    def post(self, request, *args, **kwargs):
        register_form = RegisterForm(request.POST)
        subscribe_form = SubscribeForm(request.POST)
        
        if 'subscribe' in request.POST:
            if subscribe_form.is_valid():
                subscribe_form.send_email()
                subscribe_form.save()
                
            return redirect('shop:register')
            
        else:
            if register_form.is_valid():
                return self.form_valid(register_form)
            else:
                return self.form_invalid(register_form)
            
    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get('email')
        telephone = form.cleaned_data.get('telephone')
        user = User.objects.get(email=email)
        user.username = f'app_user_{user.id}'
        user_data = UserData.objects.create(user=user, telephone=telephone)
        user_data.save()
        user.save()
        
        login(self.request, user)
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        context['subscribe_form'] = SubscribeForm()
        context['cart'] = Cart(self.request)
        return context
    
    
class ProductDetailsView(DetailView):
    model = Product
    template_name = 'shop/product_details.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        context['subscribe_form'] = SubscribeForm()
        context['cart'] = Cart(self.request)
        product = self.get_object() 
        category = product.category
        brand = product.brand
        
        
        average_rating = product.reviews.aggregate(Avg('rating'))['rating__avg']
        if average_rating is None:
            average_rating = 0
        
        context['average_rating'] = round(average_rating)
        
        breadcrumbs = [{'name': 'Main', 'url': reverse('shop:main')}]
        for parent in category.get_full_breadcrumb_path():
            breadcrumbs.append({'name': parent.name, 'url': parent.get_absolute_url()})
        breadcrumbs.append({'name': category.name, 'url': category.get_absolute_url(), 'class': 'active'})
        
        brand_breadcrumbs = [{'name': 'Brands', 'url': reverse('shop:product_brands')},
                       {'name': brand.name, 'url': brand.get_absolute_url(), 'class': 'active'}]
        
        brand_products = Product.objects.filter(
            brand=brand,
            is_available=True,
            stock__gt=0
        ).exclude(
            id=product.id
        )
        category_products = Product.objects.filter(
            category=category,
            is_available=True,
            stock__gt=0
        ).exclude(
            id=product.id
        )
        comment_form = ProductReviewForm()
        reviews = ProductReview.objects.filter(
            parent__isnull=True,
            product=product
        ).order_by('-created_at')
        
        paginator = Paginator(reviews, 4)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context['breadcrumbs'] = breadcrumbs
        context['brand_breadcrumbs'] = brand_breadcrumbs
        context['brand_products'] = brand_products
        context['category_products'] = category_products
        context['comment_form'] = comment_form
        context['page_obj'] = page_obj
        
        return context
    
    def post(self, request, id, slug):
        
        if id and slug: 
            product = get_object_or_404(Product, slug=slug, id=id)
        
        
        if 'subscribe' in request.POST:
            subscribe_form = SubscribeForm(request.POST)
            if subscribe_form.is_valid():
                subscribe_form.send_email()
                subscribe_form.save()
                messages.success(request, "You have successfully subscribed to our newsletter!")
            else:
                messages.info(request, "Invalid email or you had already subscribed to our newsletter.")
        
        elif 'toggle_wishlist' in request.POST:
            product_id = request.POST.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            wishlist, created = WishList.objects.get_or_create(user=request.user)
            if product in wishlist.products.all():
                wishlist.products.remove(product)
            else:
                wishlist.products.add(product)
                
        elif 'toggle-cart' in request.POST:
            product_id = request.POST.get('product_id')
            product = Product.objects.get(id=product_id)
            cart = Cart(self.request)
            cart.add(product)
                
                
                
        elif 'add-comment' in request.POST:
            comment_form = ProductReviewForm(request.POST)
            review_images_form = ReviewImageForm(request.POST, request.FILES)
            if comment_form.is_valid() and review_images_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.product = product
                comment.user = request.user
                comment.save()
                images = request.FILES.getlist('file-upload')
                for image in images:
                    image_ins = ReviewImage(image=image, review=comment)
                    image_ins.save()
                messages.success(request, "Your review has been submitted successfully!")
            else:
                messages.error(request, "There was an error with your review submission.")
                
        elif 'add-reply' in request.POST:
            reply_form = ReplyForm(request.POST)
            review_images_form = ReviewImageForm(request.POST, request.FILES)
            if reply_form.is_valid() and review_images_form.is_valid():
                parent_id = request.POST.get('parent')
                parent_review = get_object_or_404(ProductReview, id=parent_id)
                reply = reply_form.save(commit=False)
                reply.product = product
                reply.parent = parent_review
                reply.user = request.user
                reply.save()
                images = request.FILES.getlist('file-upload')
                for image in images:
                    image_ins = ReviewImage(image=image, review=reply)
                    image_ins.save()
                messages.success(request, "Your reply has been submitted successfully!")
            else:
                messages.error(request, "There was an error with your reply submission.")
        
        elif 'delete-comment' in request.POST:
            comment_id = request.POST.get('comment_id')
            review = get_object_or_404(ProductReview, id=comment_id)
            review.delete()
            
        elif 'notify' in request.POST:
            product_id = request.POST.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            notification, created = NotificationSubscription.objects.get_or_create(
                user=request.user,
                product=product
            )
            
            if created:
                messages.success(request, 'You will be notified when this product is back in stock.')
            else:
                messages.info(request, 'You are already subscribed for notifications for this product.')    
                     
        return redirect(f'{request.path}')
