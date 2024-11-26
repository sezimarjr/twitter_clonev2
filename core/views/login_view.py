
from django.shortcuts import render, redirect


from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth


def login_view(request):
    form = AuthenticationForm(request)
    if request.user.is_authenticated:
        return redirect('core:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            print("Usuario logou com sucesso")
            return redirect('core:index')

    return render(request, 'login.html', {'form': form})
