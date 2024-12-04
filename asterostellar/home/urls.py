from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('home/', views.index, name='home'),
    path('', views.index, name='home')
]