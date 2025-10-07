from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('catalog/', views.CatalogView.as_view(), name='catalog'),
    path('catalog/<slug:category_slug>/', views.CatalogView.as_view(), name='catalog_category'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]