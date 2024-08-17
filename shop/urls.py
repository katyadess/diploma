from django.urls import path
from . import views


urlpatterns = [
    path('', views.MainPageView.as_view(), name='main'),
    path('category/<slug:category_slug>/', views.ProductListView.as_view(), name='product_list_by_category'),
    path('search', views.SearchView.as_view(), name='shop_search'),
    path('brands', views.BrandsView.as_view(), name='product_brands'),
    path('brands/<slug:brand_slug>/', views.BrandsProductView.as_view(), name='product_list_by_brand'),
]
