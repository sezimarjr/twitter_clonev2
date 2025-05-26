from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages


@login_required
def update_profile(request):
    profile = request.user.profile
    password_error = None

    if request.method == "POST":
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 or password2:
            if password1 == password2 and password1.strip() != '':
                request.user.set_password(password1)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Senha alterada com sucesso!')
            else:
                password_error = 'As senhas não coincidem ou estão vazias.'

        # Atualiza os dados do perfil (sempre que POSTar)
        name = request.POST.get('name')
        if name is not None:
            profile.name = name

        bio = request.POST.get('bio')
        if bio is not None:
            profile.bio = bio

        if request.FILES.get('avatar'):
            profile.avatar = request.FILES['avatar']

        profile.save()

        if password_error:
            # Se erro na senha, renderiza a página com erro
            context = {
                'profile': profile,
                'password_error': password_error,
                # Adicione outros contextos que seu template precisa, ex: posts
            }
            return render(request, 'profile.html', context)
        else:
            # Se tudo OK, redireciona para o perfil
            return redirect('core:profile', username=request.user.username)

    # Se for GET, ou outro método, pode renderizar a página com dados iniciais
    context = {
        'profile': profile,
        # outros contextos
    }
    return render(request, 'profile.html', context)
