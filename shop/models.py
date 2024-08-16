from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    category_image = models.ImageField(upload_to='categories', null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

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
    category = models.ForeignKey(Category, related_name='category_products', on_delete=models.CASCADE) 
    brand = models.ForeignKey(Brand, related_name='brand_products', on_delete=models.CASCADE)
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
    

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='reviews')
    text = models.TextField()
    rating = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='comment_images', blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        if self.parent:
            return f"Reply by {self.user.username} on {self.product.name}"
        return f"Review by {self.user.username} on {self.product.name}"

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        
        
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
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