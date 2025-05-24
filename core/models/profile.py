import os
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError


def validate_image(image):
    if not image.name.endswith(('.png', '.jpg', '.jpeg')):
        raise ValidationError(
            'Formato de imagem não suportado. Por favor, envie uma imagem PNG ou JPG.')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(
        upload_to='avatars', blank=True, validators=[validate_image], default='images/user_placeholder.png')

    def save(self, *args, **kwargs):
        # Verifica se o avatar foi alterado
        if self.pk:  # Verifica se já existe um perfil no banco de dados
            old_profile = Profile.objects.get(
                pk=self.pk)  # Recupera o perfil atual
            old_avatar = old_profile.avatar

            # Se o avatar foi alterado e não for a imagem padrão
            if old_avatar != self.avatar and old_avatar != 'images/user_placeholder.png':
                # Deleta a imagem antiga
                if os.path.isfile(old_avatar.path):  # Verifica se o arquivo existe
                    os.remove(old_avatar.path)

        super(Profile, self).save(*args, **kwargs)  # Salva o novo perfil

    def __str__(self):
        return self.user.username
