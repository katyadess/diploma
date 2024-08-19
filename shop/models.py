from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.


class Category(MPTTModel):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    category_image = models.ImageField(upload_to='categories', null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

    class MPTTMeta:
        order_insertion_by = ['name']


    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])

    def get_full_breadcrumb_path(self):
        
        parents = []
        category = self
        while category.parent:
            parents.insert(0, category.parent)
            category = category.parent
        
        return parents
    
class Brand(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    country = models.CharField(max_length=200)
        
    class Meta:
        ordering = ('name',)
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_list_by_brand',
                    args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='category_products', on_delete=models.SET_NULL, null=True) 
    brand = models.ForeignKey(Brand, related_name='brand_products', on_delete=models.SET_NULL, null=True)
    brief_description = models.TextField()
    detailed_description = models.TextField()
    usage_instructions = models.TextField(null=True, blank=True)
    suitable_for = models.TextField(null=True, blank=True)
    ingredients = models.TextField()
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    main_image = models.ImageField(upload_to='products')
    second_picture = models.ImageField(upload_to='products', null=True, blank=True)
    third_picture = models.ImageField(upload_to='products', null=True, blank=True)
    forth_picture = models.ImageField(upload_to='products', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_new = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_absolute_url(self):
        return reverse('shop:product_details',
                       args=[self.id, self.slug])
    

class ProductReview(MPTTModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='reviews')
    text = models.TextField()
    rating = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='comment_images', blank=True)
    parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    class MPTTMeta:
        order_insertion_by = ['product']

    def __str__(self):
        if self.parent:
            return f"Reply by {self.user.username} on {self.product.name}"
        return f"Review by {self.user.username} on {self.product.name}"

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        
        
class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    
    is_default = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('-is_default',)
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.city}, {self.street}"
    
    
class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self) -> str:
        return f'{self.email}'
    
    class Meta:
        verbose_name = 'Subscriber'
        verbose_name_plural = 'Subscribers'
    

class WishList(models.Model):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlist_items')
    
    class Meta:
        verbose_name_plural = 'Wishlist'
        
    def __str__(self) -> str:
        return self.product.name
    
class Order(models.Model):
    
    PENDING = 'pending'
    PROCESSING = 'processing'
    SENT = 'sent'
    DELIVERED = 'delivered'
    COMPLETED = 'completed'
    CANCELED = 'canceled'
    FAILED = 'failed'
    
    STATUS_CHOICES = [
        (PENDING, 'pending'),
        (PROCESSING, 'processing'),
        (SENT, 'sent'),
        (DELIVERED, 'delivered'),
        (COMPLETED, 'completed'),
        (CANCELED, 'canceled'),
        (FAILED, 'failed'),
    ]
    
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='orders')
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, default=PENDING, max_length=50)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('created',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        
        
    def __str__(self) -> str:
        return f'order by {self.id}'
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    
    

class OrderItem(models.Model):
    
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    
    def __str__(self) -> str:
        return f'{self.id}'
    
    def get_cost(self):
        return self.price * self.quantity