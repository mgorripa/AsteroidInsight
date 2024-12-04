from django.urls import path
from . import views

app_name = 'PHA'
urlpatterns = [
    path('pha/', views.index, name='pha')
]