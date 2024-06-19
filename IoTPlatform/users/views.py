from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

# Create your views here.


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, message="Username does not exist!")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('MonitoringApp:show_graph')

    return render(request, 'users/login.html')


def user_register(request):
    if request.method == "POST":
        username = request.POST["user"]
        email = request.POST['email']
        password = request.POST["password"]
        re_password = request.POST["retype-password"]
        if password == re_password:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            return redirect('MonitoringApp:show_graph')
        else:
            messages.error(request, "Password not match")
    return render(request, 'users/register.html')


def user_logout(request):
    logout(request)
    return redirect('MonitoringApp:dashbord')

