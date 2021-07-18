from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

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
            login(request, user)
            return HttpResponseRedirect(reverse('polls:index'))
        else:
            return HttpResponseRedirect(reverse('auth:login'))


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('auth:login'))
