from django.contrib.auth.models import User
from .models import Follow


def setup_user_methods():
    """Adiciona métodos de follow ao model User"""

    def get_followers(self):
        """Retorna todos os seguidores"""
        return User.objects.filter(followers__follower=self)

    def get_following(self):
        """Retorna todos que o usuário segue"""
        return User.objects.filter(following__following=self)

    def follow(self, user):
        """Segue um usuário"""
        if self == user:
            raise ValueError("Não pode seguir a si mesmo")
        Follow.objects.get_or_create(follower=self, following=user)

    def unfollow(self, user):
        """Deixa de seguir um usuário"""
        Follow.objects.filter(follower=self, following=user).delete()

    def is_following(self, user):
        """Verifica se está seguindo"""
        return Follow.objects.filter(follower=self, following=user).exists()

    # Adiciona os métodos ao User
    User.add_to_class('get_followers', get_followers)
    User.add_to_class('get_following', get_following)
    User.add_to_class('follow', follow)
    User.add_to_class('unfollow', unfollow)
    User.add_to_class('is_following', is_following)
