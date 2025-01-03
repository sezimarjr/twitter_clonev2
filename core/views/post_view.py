from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from core.models import Post
from core.forms import PostForm
from core.models.profile import Profile

# Criar um post (somente usuários autenticados)


@login_required(login_url='core:login')
def index(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            print(f"Post criado com sucesso: {post.content}")
            return redirect('core:index')
        else:
            print(f"Formulario invalido {form.errors}")

    posts = Post.objects.all().order_by('-created_at')  # Posts recentes primeiro
    for post in posts:
        post.liked_by_user = post.likes.filter(user=request.user).exists()

    return render(request, 'index.html', {'posts': posts, 'form': form})


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
