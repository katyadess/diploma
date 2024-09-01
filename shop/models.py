from django.db import models
from django.conf import settings
from django.urls import reverse
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
    
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name
        


class ProductReview(MPTTModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='reviews')
    text = models.TextField()
    rating = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    class MPTTMeta:
        order_insertion_by = ['-created_at']

    def __str__(self):
        if self.parent:
            return f"Reply by {self.user.username} on {self.product.name}"
        return f"Review by {self.user.username} on {self.product.name}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
  
class ReviewImage(models.Model):
    image = models.FileField(upload_to='review_images')
    review = models.ForeignKey(ProductReview, related_name='review_images', on_delete=models.CASCADE)      
        
class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    is_archived = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f"""
    \n{self.first_name}\n
    \n{self.last_name}\n
    \n{self.city}\n 
    \n{self.street}\n
    """
    
    
class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self) -> str:
        return f'{self.email}'
    
    class Meta:
        verbose_name = 'Subscriber'
        verbose_name_plural = 'Subscribers'
        
        
class NotificationSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    notified = models.BooleanField(default=False) 
    
    class Meta:
        unique_together = ('user', 'product')
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        
    def __str__(self) -> str:
        return f'{self.user} notify about {self.product.name}' 

class WishList(models.Model):
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='wishlist_items', blank=True)
    
    class Meta:
        verbose_name_plural = 'Wishlist'
        
    def __str__(self) -> str:
        return f"Wishlist of {self.user.username}"
    
class UserData(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=20)
    
    class Meta:
        verbose_name = 'UserData'
        verbose_name_plural = 'UserData'
        
    def __str__(self) -> str:
        return self.user.email