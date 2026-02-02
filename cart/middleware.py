from django.utils.deprecation import MiddlewareMixin
from .models import Cart

class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.session_key:
            request.session.create()

        session_key = request.session.session_key

        cart = Cart.objects.filter(session_key=session_key).first()

        if not cart:
            cart = Cart.objects.create(session_key=session_key)

        request.cart = cart

        return self.get_response(request)
