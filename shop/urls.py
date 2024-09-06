from django.urls import path
from . import views


urlpatterns = [
    path('', views.MainPageView.as_view(), name='main'),
    
    path('category/<slug:category_slug>/', views.ProductListView.as_view(), name='product_list_by_category'),
    
    path('new_arrivals', views.NewArrivalsView.as_view(), name='new_arrivals'),
    
    path('discount_products', views.DiscountProductsView.as_view(), name='discount_products'),
    
    path('search', views.SearchView.as_view(), name='shop_search'),
    
    path('brands', views.BrandsView.as_view(), name='product_brands'),
    
    path('brands/<slug:brand_slug>/', views.BrandsProductView.as_view(), name='product_list_by_brand'),
    
    path('help', views.HelpView.as_view(), name='help'),
    
    path('contact', views.ContactView.as_view(), name='contact'),
    
    path('account', views.account, name='account'),
    
    path('logout', views.MyLogoutView.as_view(), name='shop_logout'),
    
    path('login', views.MyLoginView.as_view(), name='shop_login'),
    
    path('register', views.RegisterView.as_view(), name='register'),
    
    path('change_password', views.MyPasswordChangeView.as_view(), name='change_password'),

    path('product/<int:id>/<slug:slug>', views.ProductDetailsView.as_view(), name='product_details'),
    
]


 