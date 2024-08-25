from django.urls import path
from . import views

urlpatterns = [
    path('create_order', views.CreateOrderView.as_view(), name='order')
]
