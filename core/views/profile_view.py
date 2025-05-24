from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from core.models import Profile, Post


@login_required
def profile_view(request, username):
    user_to_view = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user_to_view)

    # Verifica se o usuário logado segue o perfil
    is_following = (request.user.is_authenticated and
                    request.user != user_to_view and
                    request.user.is_following(user_to_view))

    posts = Post.objects.filter(user=user_to_view).order_by('-created_at')
    for post in posts:
        post.liked_by_user = post.likes.filter(user=request.user).exists()
        post.total_likes = post.likes.count()

    new_users = Profile.objects.exclude(
        user=request.user).order_by('-user__date_joined')[:4]

    context = {
        'profile': profile,
        'posts': posts,
        'user': request.user,
        'new_users': new_users,
        'user_to_view': user_to_view,
        'is_following': is_following

    }

    return render(request, 'profile.html', context)
