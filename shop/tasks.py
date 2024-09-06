from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from orders.models import *

@shared_task(bind=True)
def update_pending_to_processing(self):
    
    now = timezone.now()
    
    processing_period = timedelta(minutes=1)
    
    orders_to_update = Order.objects.filter(
        status=Order.PENDING,
        created__lte=now - processing_period
    )
    
    for order in orders_to_update:
        order.status = Order.PROCESSING
        order.save()
        
    return 'Done'
        
        
@shared_task(bind=True)
def update_processing_to_sent(self):
    now = timezone.now()
    
    processing_period = timedelta(minutes=2)

    orders_to_update = Order.objects.filter(
        status=Order.PROCESSING,
        updated__lte=now - processing_period
    )

    for order in orders_to_update:
        order.status = Order.SENT
        order.save()
        
    return 'Done'


@shared_task(bind=True)
def update_sent_to_delivered(self):
    now = timezone.now()
    
    sent_period = timedelta(minutes=4)

    orders_to_update = Order.objects.filter(
        status=Order.SENT,
        updated__lte=now - sent_period
    )

    for order in orders_to_update:
        order.status = Order.DELIVERED
        order.save()
     
    return 'Done'   
        
@shared_task(bind=True)
def update_delivered_to_completed(self):
    now = timezone.now()
    
    delivered_period = timedelta(minutes=5)

    orders_to_update = Order.objects.filter(
        status=Order.DELIVERED,
        updated__lte=now - delivered_period
    )

    for order in orders_to_update:
        order.status = Order.COMPLETED
        order.save()
        
    return 'Done'
        
