from django.urls import path
from core import views
from django.contrib.auth.views import LogoutView
from django.views.generic.base import RedirectView


app_name = 'core'

urlpatterns = [
    path('home/', views.index, name='index'),
    path('profile/<str:username>', views.profile_view, name='profile'),
    path('', RedirectView.as_view(url='home/', permanent=False)),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='core:login'), name='logout'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('update-avatar/', views.update_avatar, name='update_avatar'),
    path('profile/<str:username>/follow/',
         views.toggle_follow, name='toggle_follow'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('profile/update/', views.update_profile, name='update_profile'),



]
