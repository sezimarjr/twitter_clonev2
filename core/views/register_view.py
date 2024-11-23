from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from core.models import Profile


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Cria o usuário
            user = form.save()

            # Após a criação, associamos esse usuário ao perfil
            Profile.objects.create(user=user)

            # Loga automaticamente o usuário após o registro
            login(request, user)

            # Redireciona para a página de perfil ou página inicial
            # Ajuste para o nome da view de perfil
            return redirect('profile_view')

    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})
