from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required
def update_profile(request):
    if request.method == "POST":
        profile = request.user.profile
        # <--- aqui altera o nome completo
        profile.name = request.POST.get('name')
        profile.bio = request.POST.get('bio')

        if request.FILES.get('avatar'):
            profile.avatar = request.FILES['avatar']

        profile.save()
        return redirect('core:profile', username=request.user.username)
