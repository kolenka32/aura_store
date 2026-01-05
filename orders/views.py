from django.shortcuts import render
from django.views import View

from cart.views import CartMixin


# Create your views here.
class CheckoutView(CartMixin, View):
    def get(self, request):
        cart = CartMixin().get_cart(request)

        context = {
            'cart': cart,
            'cart_items': cart.items.select_related('product', 'product_size__size').order_by('-added_at'),
            'subtotal': cart.subtotal,
        }

        return render(request, 'orders/checkout.html', context)