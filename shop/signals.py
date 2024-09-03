from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product, NotificationSubscription
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=Product)
def check_stock_and_notify(sender, instance, **kwargs):
    if instance.stock > 0:
        notifications = NotificationSubscription.objects.filter(
            product=instance, 
            notified=False
        )
        
        for n in notifications:
            try:
                send_mail(
                    'Product back in stock!',
                    f'The product {instance.name} is back in stock!',
                    settings.EMAIL_HOST_USER,
                    [n.user.email],
                    fail_silently=False,
                )
                n.delete()
            except Exception as e:
                print(f"Failed to send email to {n.user.email}: {e}")
                