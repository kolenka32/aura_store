from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views import View

from cart.views import CartMixin
from orders.forms import OrderForm
import logging

from orders.models import Order, OrderItem
from payment.views import create_stripe_checkout_session

logger = logging.getLogger(__name__)


# Create your views here.
@method_decorator(login_required(login_url='/users/login'), name='dispatch')
class CheckoutView(CartMixin, View):
    def get(self, request):
        cart = CartMixin().get_cart(request)
        logger.debug(f"Checkout view: session_key={request.session.session_key} cart_id={cart.id}")

        if cart.total_items == 0:
            logger.warning(f"Cart is empty")

            return TemplateResponse(request, 'cart/cart.html', {'cart': cart, 'title': f"AURA STORE - Корзина"})

        total_price = cart.subtotal
        logger.debug(f"total_price={total_price}")


        form = OrderForm(user=request.user)
        context = {
            'cart': cart,
            'form': form,
            'cart_items': cart.items.select_related('product', 'product_size__size').order_by('-added_at'),
            'subtotal': cart.subtotal,
            'total_price': total_price,
        }

        return render(request, 'orders/checkout.html', context)

    def post(self, request):

        cart = CartMixin().get_cart(request)
        payment_provider = request.POST.get('payment_provider')
        logger.debug(f"Checkout POST: session_key={request.session.session_key}, cart_id={cart.id}, cart_id={cart.id}")

        if cart.total_items == 0:
            logger.warning(f"Cart is empty")

            return TemplateResponse(request, 'cart/cart.html', {'cart': cart, 'title': f"AURA STORE - Корзина"})

        if not payment_provider or payment_provider not in ['stripe', 'helecet']:
            logger.info(f"Invalid payment provider: {payment_provider}")
            context = {
                'cart': cart,
                'form': OrderForm(user=request.user),
                'cart_items': cart.items.select_related('product', 'product_size__size').order_by('-added_at'),
                'total_price': cart.sub_total,
                'error_message': 'Please select your payment provider',
            }

            return TemplateResponse(request, 'orders/checkout.html', context)

        total_price = cart.subtotal
        form_data = request.POST.copy()

        if not form_data.get('email'):
            form_data['email'] = request.user.email

        form = OrderForm(data=form_data, user=request.user)

        if form.is_valid():
            order = Order.objects.create(
                first_name=form_data['first_name'],
                last_name=form_data['last_name'],
                email=form_data['email'],
                phone=form_data['phone'],
                address=form_data['address'],
            )

            for item in cart.items.select_related('product', 'product_size__size').order_by('-added_at'):
                logger.debug(f"Processing cart item: item={item.id}, total_price={total_price}, size={item.product_size.size}")
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    size=item.product_size.size,
                    quantity=item.quantity,
                    price=item.price or Decimal('0.00'),
                )

            try:
                logger.info(f"Creating payment session for provider: {payment_provider}")
                if payment_provider == 'stripe':
                    logger.info(f"Creating payment session for provider: {payment_provider}")
                    checkout_session = create_stripe_checkout_session(request, order)
                    cart.clear()
                    try:
                        response = HttpResponse(status=200)
                        response['HX-Redirect'] = checkout_session.url
                        logger.info(f"Creating payment session for provider: {payment_provider}")
                        return response
                    except:
                        return redirect(checkout_session.url)

            except Exception as e:
                logger.error(f"Error creating payment: {str(e)}", exc_info=True)
                order.delete()
                context = {
                    'cart': cart,
                    'form': form,
                    'cart_items': cart.items.select_related('product', 'product_size__size').order_by('-added_at'),
                    'total_price': total_price,
                    'error_message': str(e),
                }

                return TemplateResponse(request, 'orders/checkout.html', context)
        else:
            logger.error(f"Invalid form: {form.errors}")
            context = {
                'cart': cart,
                'form': form,
                'cart_items': cart.items.select_related('product', 'product_size__size').order_by('-added_at'),
                'total_price': total_price,
                'error_message': form.errors,
            }

            return TemplateResponse(request, 'orders/checkout.html', context)















