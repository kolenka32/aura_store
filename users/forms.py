from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, authenticate
from django.utils.html import strip_tags
from django.core.validators import RegexValidator

User = get_user_model()



from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'address', 'phone')


class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Email', widget=forms.TextInput(attrs={
        'class': 'dotted-input w-full py-3 text-sm font-medium text-gray-900 placeholder-gray-500',
        'placeholder': 'EMAIL',
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'dotted-input w-full py-3 text-sm font-medium text-gray-900 placeholder-gray-500',
        'placeholder': 'PASSWORD'
    }))

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError('Invalid email or password')
            elif not self.user_cache.is_active:
                raise forms.ValidationError('This account is inactive')
        return self.cleaned_data
