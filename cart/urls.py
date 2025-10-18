from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('add/<slug:slug>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('update/<int:item_id>/', views.UpdateCartItemView.as_view(), name='update_cart_quantity'),

    path('remove/<int:item_id>/', views.RemoveCartItemView.as_view(), name='remove_cart_quantity'),
    path('delete/<int:item_id>/', views.DeleteCartItemView.as_view(), name='delete_item'),
]