from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()


class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={
        'id': 'username',
        'name': 'username',
        'type': 'text',
        'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-gray-500 focus:border-gray-500 transition duration-200',
        'placeholder': 'your@email.com'}))

    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'id': 'password',
        'name': 'password',
        'type': 'password',
        'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-gray-500 focus:border-gray-500 transition duration-200 pr-10',
        'placeholder': '********',
    }))


    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError('Incorrect username or password.')
            elif not self.user_cache.is_active:
                raise forms.ValidationError('This account is inactive.')
            return self.cleaned_data


class CustomUserCreationForm(forms.ModelForm):
    ...

class CustomUserUpdateForm(forms.ModelForm):
    ...