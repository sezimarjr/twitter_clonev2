from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from core.models import Post, Like


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    liked_by_user = post.likes.filter(user=request.user).exists()

    return JsonResponse({'liked': liked, 'total_likes': post.total_likes(), 'liked_by_user': liked_by_user})
