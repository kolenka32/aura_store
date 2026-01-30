from django.contrib.auth import get_user_model, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.views import View

from users.forms import CustomUserUpdateForm, CustomUserLoginForm


# Create your views here.

def register(request):
    if request.method == 'POST':
        form =
    return render(request, 'users/register.html')


def login_view(request):
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
    return TemplateResponse(request, 'users/login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('products:index')


@login_required(login_url='/users/login/')
def profile(request):

    return render(request, 'users/profile.html')