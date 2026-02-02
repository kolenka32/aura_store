from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.generic import View
from django.contrib import messages

from products.models import ProductSize, Product
from .forms import AddToCartForm
from .models import Cart, CartItem

from .utils import get_cart


# Create your views here.



class CartView(LoginRequiredMixin, View):
    login_url = 'users:login'
    def get(self, request):
        cart = get_cart(request)
        
        context = {
            'title': 'AURA STORE',
            'cart': cart,
            'cart_items': cart.items.select_related('product', 'product_size').order_by('-added_at'),
            'total_price': cart.subtotal,
            'total_items': cart.total_items,
        }
        
        return TemplateResponse(request, 'cart/cart.html', context)


class AddToCartView(View):
    @transaction.atomic()
    def post(self, request, slug):
        cart = get_cart(request)
        product = get_object_or_404(Product, slug=slug)
        can_add_to_cart = True
        
        message = None
        
        form = AddToCartForm(request.POST, product=product)

        if not form.is_valid():
            print(form.errors)
            message = 'Invalid form'
            can_add_to_cart = False
            

        size_id = form.cleaned_data.get('size_id')
        if size_id:
            product_size = get_object_or_404(ProductSize, id=size_id)
            message = f"Product {product.name} ({product_size.size}) added to cart"

        else:
            product_size = product.product_sizes.filter(stock__gt=0).first()
            if not product_size:
                message = 'No sizes available'
                can_add_to_cart = False


        quantity = form.cleaned_data.get('quantity')
        if quantity > product_size.stock:
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


class UpdateCartItemView(View):
    @transaction.atomic()
    def post(self, request, item_id):

        message = None
        try:
            cart = get_cart(request)
            cart_item = get_object_or_404(CartItem, id=item_id)

            if cart_item.quantity >= cart_item.product_size.stock:
                message = f"Only {cart_item.product_size.stock} items in stock available"

            else:
                cart_item.quantity += 1
                cart_item.save()

                request.session['cart_id'] = cart.id
                request.session.modified = True

        except CartItem.DoesNotExist:
            message = 'Item does not exists'


        if message is not None:
            messages.success(request, message)
        return redirect('cart:cart')



class RemoveCartItemView(View):
    @transaction.atomic()
    def post(self, request, item_id):
        message = None
        try:
            cart = get_cart(request)
            cart_item = get_object_or_404(CartItem, id=item_id)

            if cart_item.quantity == 1:
                cart_item.delete()
                message = f"Product {cart_item.product.name} deleted"

            elif cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()


            request.session['cart_id'] = cart.id
            request.session.modified = True


        except CartItem.DoesNotExist:
            message = 'Item does not exists'

        if message is not None:
            messages.success(request, message)

        return redirect('cart:cart')


class DeleteCartItemView(View):
    @transaction.atomic()
    def post(self, request, item_id):
        try:
            cart = get_cart(request)
            cart_item = get_object_or_404(CartItem, id=item_id)

            cart_item.delete()
            message = f"Product {cart_item.product.name} deleted"

            request.session['cart_id'] = cart.id
            request.session.modified = True

        except CartItem.DoesNotExist:
            message = 'error'


        if message != 'error':
            messages.success(request, message)

        return redirect('cart:cart')
       