from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def register(request):
    if request.method == 'POST':
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if password == confirm_password:
                User.objects.create_user(
                    username=username, 
                    password=password, 
                    first_name=first_name, 
                    last_name=last_name,
                    )
                print(1111)
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('auth:register')
        except:
            return redirect('auth:register')
    return render(request, 'auth/register.html')

def log_in(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard:index')
            else:
                return render(request,'auth/login.html')
        except:
            return redirect('auth:login')
    return render(request, 'auth/login.html')

def log_out(request):
    logout(request)
    return redirect('auth:login')

