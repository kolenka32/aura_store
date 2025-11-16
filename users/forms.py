from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.template.context_processors import request

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
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError('Incorrect username or password.')
            elif not self.user_cache.is_active:
                raise forms.ValidationError('This account is inactive.')
            return self.cleaned_data




class CustomUserCreationForm(forms.ModelForm):
    ...



class CustomUserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={
        'id': 'first_name',
        'name': 'first_name',
        'type': 'text',
        'required': True,
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-sm text-sm focus:outline-none focus:border-black focus:ring-0 transition-colors duration-200',
        'placeholder': 'Имя...'
    }))

    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={
        'id': 'last_name',
        'name': 'last_name',
        'type': 'text',
        'required': True,
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-sm text-sm focus:outline-none focus:border-black focus:ring-0 transition-colors duration-200',
        'placeholder': 'Фамилия...'
    }))

    email = forms.EmailField(label='Почта', widget=forms.EmailInput(attrs={
        'id': 'email',
        'name': 'email',
        'type': 'email',
        'required': True,
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-sm text-sm focus:outline-none focus:border-black focus:ring-0 transition-colors duration-200',
        'placeholder': 'email...',
    }))

    phone = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={
        'id': 'phone',
        'name': 'phone',
        'type': 'text',
        'required': True,
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-sm text-sm focus:outline-none focus:border-black focus:ring-0 transition-colors duration-200',
        'placeholder': 'phone number...'
    }))

    address = forms.CharField(label='Адрес', widget=forms.Textarea(attrs={
        'rows': '3',
        'id': 'address',
        'name': 'address',
        'type': 'text',
        'required': True,
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-sm text-sm focus:outline-none focus:border-black focus:ring-0 transition-colors duration-200',
        'placeholder': 'address...',
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'address')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['address'].initial = self.instance.address1


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('This email is already in use.')
        return email



