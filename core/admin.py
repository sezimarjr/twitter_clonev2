from django.contrib import admin

from core.models.post import Post
from .models import Profile

# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'location', 'birth_date',
                    'avatar')  # Campos que você quer ver na lista
    # Campos para pesquisa
    search_fields = ('user__username', 'bio', 'location')
    list_filter = ('location',)  # Filtros para a barra lateral do admin


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_at')
