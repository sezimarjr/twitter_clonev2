from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from core.models import Post
from core.forms import PostForm

# Criar um post (somente usuários autenticados)


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Associar o post ao usuário autenticado
            post.save()
            return redirect('post_list')  # Redireciona para a lista de posts
    else:
        form = PostForm()
    # return render(request, 'post_form.html', {'form': form})
    return 'post_create'

# Listar todos os posts


def post_list(request):
    posts = Post.objects.all()
    # return render(request, 'post_list.html', {'posts': posts})
    return 'post_list'

# Detalhar um post específico


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # return render(request, 'post_detail.html', {'post': post})
    return 'post_detail'

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
