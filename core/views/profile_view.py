from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from core.models import Profile
from core.models.post import Post


@login_required  # Adicione este decorator para garantir usuário logado
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)

    posts = Post.objects.filter(user=user).order_by('-created_at')

    # Adiciona a informação de curtida para cada post
    for post in posts:
        post.liked_by_user = post.likes.filter(user=request.user).exists()
        post.total_likes = post.likes.count()

    new_users = Profile.objects.exclude(
        user=request.user).order_by('-user__date_joined')[:4]

    context = {
        'profile': profile,
        'posts': posts,
        'user': request.user,
        'new_users': new_users
    }

    return render(request, 'profile.html', context)
