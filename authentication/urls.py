from django.urls import path

from . import views

app_name = 'auth'
urlpatterns = [
    # ex: /auth/login
    path('login', views.login_user, name='login'),
]