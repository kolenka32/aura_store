from django import forms
from django.db import models
from django.utils.html import strip_tags


class OrderForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': "w-full px-4 py-3 rounded-none border border-gray-400 bg-white text-gray-900 focus:outline-none focus:border-gray-800 focus:ring-0 transition-colors placeholder:text-gray-500",
        'placeholder': 'Имя...',
        'type': 'text',
        'name': 'first_name',
        'required': True,


    }))
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            self.fields['phone'].initial = user.phone
            self.fields['address'].initial = user.address


    def clean(self):
        cleaned_data = super().clean()
        for field in ['first_name', 'last_name', 'email', 'phone', 'address']:
            if cleaned_data.get(field):
                cleaned_data[field] = strip_tags(cleaned_data[field])
        return cleaned_data