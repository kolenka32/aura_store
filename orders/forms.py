from django import forms
from django.utils.html import strip_tags



class OrderForm(forms.Form):
    first_name = forms.CharField(
        label='ИМЯ', max_length=100, required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-none border border-gray-400 bg-white text-gray-900 focus:outline-none focus:border-gray-800 focus:ring-0 transition-colors placeholder:text-gray-500',
            'placeholder': 'ИВАН',
        })
    )

    last_name = forms.CharField(
        label='ФАМИЛИЯ', max_length=100, required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-none border border-gray-400 bg-white text-gray-900 focus:outline-none focus:border-gray-800 focus:ring-0 transition-colors placeholder:text-gray-500',
            'placeholder': 'ИВАНОВ',
        })
    )

    email = forms.EmailField(
        label='EMAIL', required=True, widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 rounded-none border border-gray-400 bg-white text-gray-900 focus:outline-none focus:border-gray-800 focus:ring-0 transition-colors placeholder:text-gray-500',
            'placeholder': 'example@mail.ru',
        })
    )

    phone = forms.CharField(
        label='ТЕЛЕФОН', max_length=20, required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-none border border-gray-400 bg-white text-gray-900 focus:outline-none focus:border-gray-800 focus:ring-0 transition-colors placeholder:text-gray-500',
            'placeholder': '+7 (999) 123-45-67',
        })
    )

    address = forms.CharField(
        label='АДРЕС ДОСТАВКИ', max_length=255, required=True,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-3 rounded-none border border-gray-400 bg-white text-gray-900 focus:outline-none focus:border-gray-800 focus:ring-0 transition-colors placeholder:text-gray-500 resize-none',
            'placeholder': 'г. Москва, ул. Примерная, д. 10, кв. 25',
            'rows': 3,
        })
    )


    def __init__(self, *args, user=None , **kwargs):
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
