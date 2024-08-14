from django.urls import path
from . import views


urlpatterns = [
    path('', views.MainPageView.as_view(), name='main'),
    path('<slug:category_slug>/', views.ProductListView.as_view(), name='product_list_by_category'),
]
