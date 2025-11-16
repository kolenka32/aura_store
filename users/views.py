from django.contrib import messages
from django.contrib.auth import get_user_model, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from users.forms import CustomUserUpdateForm, CustomUserLoginForm, CustomUserCreationForm


# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            print(user)
            return redirect('users:profile')
        else:
            print(form.errors)
    else:
        form = CustomUserLoginForm()
    return render(request, 'users/login.html', {'form': form, 'title': 'Aura Store - login'})



def logout_view(request):
    logout(request)
    return redirect('users:login')


@login_required(login_url='/users/login/')
def profile(request):

    if request.method == 'POST':
        form = CustomUserUpdateForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, 'Es un error')
    else:
        form = CustomUserUpdateForm(instance=request.user)

    context = {
        'title': f"{request.user.username}",
        'form': form,
    }

    return render(request, 'users/profile.html', context)



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
        else:
            messages.error(request, 'Es un error')
            print(form.errors)
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
        'title': f"Aura Store - register",
    }

    return render(request, 'users/register.html', context)


