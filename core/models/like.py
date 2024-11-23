from django.db import models
from django.contrib.auth.models import User
from core.models import Post


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Quem curtiu
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='likes')  # Post curtido

    class Meta:
        # Impede que o mesmo usuário curta o mesmo post mais de uma vez
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} curtiu {self.post.id}"
