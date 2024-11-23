from django.urls import path
from core import views


app_name = 'core'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
]
