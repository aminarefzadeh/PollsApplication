from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView
from authentication.forms import UserForm

# Create your views here.
from django.urls import reverse


def login_user(request):
    if request.method == 'GET':
        return HttpResponse(render(request, 'login.template'))
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is not None:
            if request.user.is_authenticated:
                logout(request)
            login(request, user)
            return HttpResponseRedirect(reverse('polls:index'))
        else:
            return HttpResponseRedirect(reverse('auth:login'))


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('auth:login'))


class Register(CreateView):
    model = User
    form_class = UserForm
    template_name = 'register.template'
    success_url = settings.LOGIN_URL
