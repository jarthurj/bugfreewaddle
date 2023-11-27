from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.login_user,name="login_user"),
    path('register/',views.register, name="register"),
    path('create_user/', views.create_user, name="create_user"),
    path('logout/',views.logout_user, name='logout')
]
