from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from .models import Profile, Follow  # Adicione o Follow aqui
from PIL import Image

# Signal original (cria perfil automaticamente)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Signal original (salva perfil após atualização)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

# ⭐ NOVO SIGNAL (Adiciona métodos de follow ao User) ⭐


@receiver(post_save, sender=User)
def add_follow_methods(sender, instance, **kwargs):
    """Adiciona métodos de follow/unfollow ao model User."""

    def get_followers(self):
        """Retorna todos os seguidores do usuário."""
        return User.objects.filter(followers__follower=self)

    def get_following(self):
        """Retorna todos que o usuário segue."""
        return User.objects.filter(following__following=self)

    def follow(self, user):
        """Usuário segue outro usuário."""
        if self == user:
            raise ValueError("Você não pode seguir a si mesmo! 🤦‍♂️")
        follow, created = Follow.objects.get_or_create(
            follower=self,
            following=user
        )
        return follow

    def unfollow(self, user):
        """Usuário para de seguir outro usuário."""
        Follow.objects.filter(follower=self, following=user).delete()

    def is_following(self, user):
        """Verifica se o usuário segue outro."""
        return Follow.objects.filter(follower=self, following=user).exists()

    # Adiciona os métodos ao model User (só uma vez!)
    if not hasattr(User, 'get_followers'):
        User.add_to_class('get_followers', get_followers)
        User.add_to_class('get_following', get_following)
        User.add_to_class('follow', follow)
        User.add_to_class('unfollow', unfollow)
        User.add_to_class('is_following', is_following)
