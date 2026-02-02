from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse

from cart.utils import attach_cart_to_user
from users.forms import CustomUserLoginForm, CustomUserCreationForm, CustomUserUpdateForm


# Create your views here.
@login_required(login_url='/users/login/')
def profile(request, tab='info'):
    user = request.user
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
    else:
        form = CustomUserUpdateForm(instance=user)

    context = {
        'title': f'ПРОФИЛЬ {user.first_name} {user.last_name}',
        'form': form,
        'tab': tab,
    }

    return TemplateResponse(request, 'users/profile.html', context)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }

    return TemplateResponse(request, 'users/register.html', context)


def login_view(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            attach_cart_to_user(request)
            return redirect('users:profile')
        else:
            print(form.errors)
    else:
        form = CustomUserLoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)

    return redirect('users:login')