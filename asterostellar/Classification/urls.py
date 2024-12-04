from django.urls import path
from . import views

app_name = 'Classification'
urlpatterns = [
    path('classification/', views.index, name='classification'),
]