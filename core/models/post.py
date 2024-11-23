from django.db import models
from django.contrib.auth.models import User


# Modelo de Post (Tweet)

class Post (models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def total_likes(self):
        """
        Método para contar o número total de curtidas para este post.
        """
        return self.likes.count()

    def __str__(self):
        return self.content[:50]
