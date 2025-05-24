from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST  # Adicione esta importação


@login_required
def toggle_follow(request, username):
    user_to_toggle = get_object_or_404(User, username=username)

    if request.user == user_to_toggle:
        return redirect('core:profile', username=username)

    if request.user.is_following(user_to_toggle):
        request.user.unfollow(user_to_toggle)
    else:
        request.user.follow(user_to_toggle)

    return redirect('core:profile', username=username)
