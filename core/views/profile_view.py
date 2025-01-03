from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from core.models import Profile
from core.models.post import Post


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)

    posts = Post.objects.filter(user=user).order_by('-created_at')
    return render(request, 'profile.html', {'profile': profile, 'posts': posts})
