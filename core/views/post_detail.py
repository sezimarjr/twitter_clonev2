from core.models import Post, Comment
from core.forms import CommentForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from core.models import Post, Comment, Profile
from core.forms import CommentForm


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('-created_at')

    post.liked_by_user = post.likes.filter(user=request.user).exists()
    post.total_likes = post.likes.count()
    post.total_comments = post.comments.count()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('core:post_detail', pk=post.pk)
    else:
        form = CommentForm()

    new_users = Profile.objects.exclude(
        user=request.user).order_by('-user__date_joined')[:4]

    return render(request, 'post_detail.html', {
        'post': post,
        'new_users': new_users,
        'comments': comments,
        'form': form,
    })
