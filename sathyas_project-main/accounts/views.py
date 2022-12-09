from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if request.user.is_authenticated:
            messages.error(request, 'You are already logged in.')
            return redirect('/')
        user = authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            # messages.success(request, 'Successfully logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Please provide valid credentials!')
            return redirect('login')
    
    else:
        return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')


        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Email is Already Taken.')
                return redirect('signup')
            else:
                user = User()
                user.username = username
                user.first_name = first_name
                user.last_name = last_name
                user.set_password(password1)
                user.save()
                messages.success(request, 'Account Created Successfully.')
                return redirect('login')
        else:
            messages.error(request, 'Password did not match!')
            return redirect('signup')

    else:
        return render(request, 'signup.html')


@login_required(login_url='login')
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('login')
    else:
        messages.error(request, 'You must be logged in!')
        return redirect('login')