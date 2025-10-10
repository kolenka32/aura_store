from django import forms
from .models import CartItem


class AddToCartForm(forms.Form):
    size_id = forms.IntegerField(required=True)
    quantity = forms.IntegerField(min_value=1, initial=1)

    def __init__(self, *args, product=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.product = product



class UpdateCartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.product_sizes:
            self.fields['quantity'].validators.append(
                forms.validators.MaxValueValidator(self.instance.product_sizes.stock)
            )