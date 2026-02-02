from django.db import models
from django.contrib.sessions.models import Session
from products.models import Product, ProductSize
from decimal import Decimal

from users.models import CustomUser


class Cart(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='carts',
        null=True,
        blank=True
    )

    session_key = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.created_at}"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        return Decimal(sum(item.quantity * item.product.price for item in self.items.all()))

    def add_product(self, product, product_size, quantity=1):
        cart_item, created = CartItem.objects.get_or_create(
            cart=self,
            product=product,
            product_size=product_size,
            defaults={'quantity': quantity},
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return cart_item

    def remove_item(self, item_id):
        try:
            item = self.items.get(id=item_id)
            item.delete()
            return True

        except CartItem.DoesNotExist:
            return False

    def update_item_quantity(self, item_id, quantity):
        try:
            item = self.items.get(id=item_id)
            if quantity > 0:
                item.quantity = quantity
                item.save()
            else:
                item.delete()
            return True

        except CartItem.DoesNotExist:
            return False

    def clear(self):
        self.items.all().delete()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['cart', 'product', 'product_size']

    def __str__(self):
        return f"{self.product.name} - {self.product_size.size} x {self.quantity}"

    @property
    def total_price(self):
        return Decimal(str(self.product.price)) * self.quantity