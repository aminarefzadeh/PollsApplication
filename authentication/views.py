from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from authentication.forms import UserForm


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


def register(request):
    if request.method == 'GET':
        form = UserForm()
        return HttpResponse(render(request, 'register.template', context={'form': form}))
    if request.method == 'POST':
        form = UserForm(data=request.POST)
        if not form.is_valid():
            print(form.errors)
            return HttpResponse(render(request, 'register.template', context={'form': form}))
        try:
            user = User.objects.create(
                username=form.cleaned_data.get('username'),
                email=form.cleaned_data.get('email'),
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name')
            )
            user.set_password(form.cleaned_data.get('password'))
            user.save()
        except Exception as e:
            print(e)
            return HttpResponseRedirect(reverse('auth:register'))
        return HttpResponseRedirect(reverse('auth:login'))
