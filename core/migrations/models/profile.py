from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError


# Modelo do Perfil


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
        upload_to='avatar', blank=True, validators=[validate_image])

    def __str__(self):
        return self.user.username
