from django.urls import path
from . import views


urlpatterns = [
    path('', views.MainPageView.as_view(), name='main'),
    
    path('category/<slug:category_slug>/', views.ProductListView.as_view(), name='product_list_by_category'),
    
    path('new_arrivals', views.NewArrivalsView.as_view(), name='new_arrivals'),
    
    path('search', views.SearchView.as_view(), name='shop_search'),
    
    path('brands', views.BrandsView.as_view(), name='product_brands'),
    
    path('brands/<slug:brand_slug>/', views.BrandsProductView.as_view(), name='product_list_by_brand'),
    
    path('help', views.HelpView.as_view(), name='help'),
    
    path('contact', views.ContactView.as_view(), name='contact'),
    
    path('account', views.AccountView.as_view(), name='account'),
]
