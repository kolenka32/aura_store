import os

from django.shortcuts import render
import stripe
import requests
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from orders.models import Order
from cart.views import CartMixin
from decimal import Decimal
import json
import hashlib
import base64

stripe_api_key = settings.STRIPE_SECRET_KEY
stripe_endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

def create_stripe_checkout_session(request, order):
    cart = CartMixin().get_cart(request)
    line_items = []
    for item in cart.items.select_related('product', 'product_size__size'):
        line_items.append({
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': f'{item.product.name} - {item.product_size.size.name}',
                },
                'unit_amount': int(item.product.price * 100),
            },
            'quantity': int(item.quantity),
        })

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri('/payment/stripe/success/') + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri('/payment/stripe/cancel/') + f'order_id={order.id}',
            metadata={
                'order_id': order.id
            }
        )

        order.stripe_payment_intend_id = checkout_session.payment_intent
        order.payment_provider = 'stripe'
        order.save()
        return checkout_session

    except Exception as e:
        raise

@csrf_exempt
@require_POST
def stripe_webhook(request):
    ...


def stripe_success(request):
    ...


def stripe_cancel(request):
    order_id = request.GET.get('order_id')
    if order_id:
        order = get_object_or_404(Order, id=order_id)
        order.status = 'canceled'
        order.save()
        context = {'order': order}

        return TemplateResponse(request, 'payment/stripe_cancel_content.html', context)
    return redirect('orders:checkout')