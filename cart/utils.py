from cart.models import Cart
from users.models import CustomUser


def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()

        cart, created = Cart.objects.get_or_create(
            session_key=request.session.session_key
        )

    return cart


def attach_cart_to_user(request):
    session_key = request.session.session_key

    if not session_key:
        return

    try:
        session_cart = Cart.objects.get(session_key=session_key, user__isnull=True)
    except Cart.DoesNotExist:
        return

    user_cart, created = Cart.objects.get_or_create(user=request.user)

    for item in session_cart.items.all():
        user_cart.add_product(item.product, item.product_size, item.quantity)

    session_cart.delete()
