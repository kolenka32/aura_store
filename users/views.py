from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from users.forms import CustomUserUpdateForm, CustomUserLoginForm


# Create your views here.

def login(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('main:index')
        else:
            print(form.errors)
    else:
        form = CustomUserLoginForm()
    return render(request, 'users/login.html', {'form': form})

def register(request):
    ...

def logout_view(request):
    logout(request)
    return redirect('products:index')
    # return render(request, 'users/logout.html')

def register(request):
    return render(request, 'users/register.html')


@login_required(login_url='/users/login/')
def profile(request):

    return render(request, 'users/profile.html')