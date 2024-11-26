from django.urls import path
from core import views
from django.contrib.auth.views import LogoutView
from django.views.generic.base import RedirectView


app_name = 'core'

urlpatterns = [
    path('home/', views.index, name='index'),
    path('', RedirectView.as_view(url='home/', permanent=False)),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='core:login'), name='logout'),
]
