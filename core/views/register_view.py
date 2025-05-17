from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from core.forms import RegisterForm
from core.models import Profile
from django.contrib import messages
from django.db import IntegrityError


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(
                    request, 'Registration successful! Please log in.')
                return redirect('core:login')
            except IntegrityError:
                messages.error(
                    request, 'Username already exists. Please choose another.')
    else:
        form = RegisterForm()  # Formulário vazio para GET

    return render(request, 'register.html', {'form': form})
