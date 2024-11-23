from django.db import models
from django.contrib.auth.models import User


class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following')  # Quem está seguindo
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers')  # Quem está sendo seguido
    created_at = models.DateTimeField(
        auto_now_add=True)  # Quando começou a seguir

    class Meta:
        # Impede que um usuário siga o mesmo usuário mais de uma vez
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.username} segue {self.following.username}"
