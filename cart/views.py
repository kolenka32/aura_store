from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.generic import View
from django.contrib import messages

from products.models import ProductSize, Product
from .forms import AddToCartForm, UpdateCartItemForm
from .models import Cart, CartItem



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

class CartView(CartMixin, View):
    def get(self, request):
        cart = self.get_cart(request)
        
        context = {
            'title': 'AURA STORE',
            'total_items': cart.total_items,
            'cart_items': cart.items.select_related('product', 'product_size__size').order_by('-added_at'),
            'total_price': cart.subtotal,
        }
        
        return TemplateResponse(request, 'cart/cart.html', context)


class AddToCartView(CartMixin, View):
    @transaction.atomic()
    def post(self, request, slug):
        cart = self.get_cart(request)
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


class UpdateCartItemView(CartMixin, View):
    @transaction.atomic()
    def post(self, request, item_id):
        cart = self.get_cart(request)
        message = None
        try:

            cart_item = get_object_or_404(CartItem, id=item_id)

            form = UpdateCartItemForm(request.POST)

            if not form.is_valid():
                message = 'Error'

            try:
                operator = form.cleaned_data.get('+')
            except:
                operator = form.cleaned_data.get('-')

            print(operator)


        except CartItem.DoesNotExist:
            message = f"Item not found"

        context = {
            'cart': cart,
            'cart_items': cart.items.select_related('product', 'product_size').order_by('-added_at'),
            'total_price': cart.subtotal,
            'total_items': cart.total_items,
            'message': message,
        }

        return TemplateResponse(request, 'cart/cart.html', context)
    
    
    

class RemoveCartItemView(CartMixin, View):
    @transaction.atomic()
    def post(self, request, item_id):
        cart = self.get_cart(request)
        try:
            cart_item = get_object_or_404(CartItem, id=item_id)
            cart_item.delete()

            request.session['cart_id'] = cart.id
            request.session.modified = True

            message = f"Item {cart_item.product.name} ({cart_item.product_size.size}) deleted"


        except CartItem.DoesNotExist:
            message = f"Item not found"
            
        
        
        context = {
            'cart': cart,
            'cart_items': cart.items.select_related('product', 'product_size').order_by('-added_at'),
            'total_price': cart.subtotal,
            'total_items': cart.total_items,
            'message': message,
        }
    
        messages.success(request, message)    
        return TemplateResponse(request, 'cart/cart.html', context)

       