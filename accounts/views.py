from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .forms import LoginForm, RegistrationForm


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            pass
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

def user_profile(request):
    user = request.user
    profile = getattr(user, 'profile', None)
    if request.method == 'POST':
        if 'phone_number' in request.POST:
            phone_number = request.POST.get('phone_number')
            if phone_number and profile:
                profile.phone_number = phone_number
                profile.save()
                return redirect('user_profile')

        elif 'add_address' in request.POST:
            address = request.POST.get('address')
            if address and profile:
                profile.address = address
                profile.save()
                return redirect('user_profile')

        elif 'add_gender' in request.POST:
            gender = request.POST.get('gender')
            if gender and profile:
                profile.gender = gender
                profile.save()
                return redirect('user_profile')
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'username': user.username,
        'phone_number': profile.phone_number if profile else '',
        'address': profile.address if profile else '',
        'gender': profile.gender if profile else ''}
    return render(request, 'accounts/user.html', context)
