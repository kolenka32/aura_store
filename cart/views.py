from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.generic import View
from django.contrib import messages

from products.models import ProductSize
from .forms import AddToCartForm
from .models import Cart, Product


# Create your views here.


class CartMixin():
    def get_cart(self, request):
        if hasattr(request, 'cart'):
            return request.cart

        if not request.session.session_key:
            request.session.create()


        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)

        request.session['cart_id'] = cart.id
        request.session.modified = True
        return cart



class AddToCartView(CartMixin, View):
    @transaction.atomic()
    def post(self, request, slug):
        cart = self.get_cart(request)
        product = get_object_or_404(Product, slug=slug)
        can_add_to_cart = True

        message = f"Product {product.name} added to cart"
        
        form = AddToCartForm(request.POST, product=product)

        if not form.is_valid():
            print(form.errors)
            message = 'Invalid form'
            can_add_to_cart = False
            

        size_id = form.cleaned_data.get('size_id')
        if size_id:
            product_size = get_object_or_404(ProductSize, id=size_id)
        else:
            product_size = product.product_sizes.filter(stock__gt=0).first()
            if not product_size:
                message = 'No sizes available'
                can_add_to_cart = False




        quantity = form.cleaned_data.get('quantity')
        if product_size.stock < quantity:
            message = f"Only {product_size.stock} sizes available"
            can_add_to_cart = False


        existing_item = cart.items.filter(product=product, product_size=product_size).first()
        if existing_item:
            total_quantity = existing_item.quantity + quantity
            if total_quantity > product_size.stock:
                message = f"Cannot add {quantity} items. Only {product_size.stock - existing_item.quantity} more available."
                can_add_to_cart = False
                
                
        if can_add_to_cart:
            cart_item = cart.add_product(product, product_size, quantity)


        print(form.errors)
        request.session['cart_id'] = cart.id
        request.session.modified = True


        messages.success(request, message)
        return redirect('products:product_detail', slug=product.slug)
