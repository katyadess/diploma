from django.db import models
from shop.models import *
# Create your models here.

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
    
