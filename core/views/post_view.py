from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from core.models import Post
from core.forms import PostForm
from core.models.profile import Profile
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required(login_url='core:login')
def index(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('core:index')

    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 10)  # Mostra 10 por página
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'has_next': False}, status=200)
        page_obj = paginator.page(paginator.num_pages)

    for post in page_obj:
        post.liked_by_user = post.likes.filter(user=request.user).exists()

    new_users = Profile.objects.exclude(
        user=request.user).order_by('-user__date_joined')[:4]

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'partials/post_list.html', {
            'posts': page_obj,
        })

    return render(request, 'index.html', {
        'form': form,
        'posts': page_obj,
        'new_users': new_users,
    })


# Editar um post (somente o dono do post pode editar)


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user != request.user:  # Verifica se o usuário é o dono do post
        return HttpResponseForbidden("Você não tem permissão para editar este post.")

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'post_form.html', {'form': form})

# Deletar um post (somente o dono do post pode excluir)


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user != request.user:  # Verifica se o usuário é o dono do post
        return HttpResponseForbidden("Você não tem permissão para excluir este post.")

    if request.method == "POST":
        post.delete()
        return redirect('post_list')
    return render(request, 'post_confirm_delete.html', {'post': post})
