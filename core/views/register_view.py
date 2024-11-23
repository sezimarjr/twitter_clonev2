from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from core.forms import RegisterForm
from core.models import Profile
from django.contrib import messages


def register(request):
    form = RegisterForm(request.POST)

    if form.is_valid():
        form.save()
        print("Registrado com sucesso")
        return redirect('core:login')

    return render(request, 'register.html', {'form': form})
