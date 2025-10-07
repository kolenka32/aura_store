from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('/add/<slug:slug>/', views.AddToCartView.as_view(), name='add_to_cart')
]