from django.urls import path, include
from . import views


urlpatterns = [

    path('login/', views.user_login, name='user-login'),
    path('logout/', views.user_logout, name='user-logout'),
    path('register/', views.user_register, name='user-register'),

]
