from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse

from users.forms import CustomUserLoginForm, CustomUserCreationForm


# Create your views here.
@login_required(login_url='/users/login/')
def profile(request):

    user = request.user
    context = {
        'title': f'ПРОФИЛЬ {user.first_name} {user.last_name}',
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
            return redirect('users:profile')
        else:
            print(form.errors)
    else:
        form = CustomUserLoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)

    return redirect('users:login')


def profile_orders(request):
    user = request.user
    context = {
        'title': f'ПРОФИЛЬ {user.first_name} {user.last_name}',
    }
    return TemplateResponse(request, 'users/profile_orders.html', context)