from django.contrib.auth import logout
from django.urls import path

from . import views

app_name = 'auth'
urlpatterns = [
    # ex: /auth/login
    path('login', views.login_user, name='login'),
    # /auth/logout
    path('logout', views.logout_user, name='logout'),
    # /auth/register
    path('register', views.register, name='register'),
]