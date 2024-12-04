from django.urls import path
from . import views

app_name = 'Solar_Distance'
urlpatterns = [
    path('solar_distance/', views.index, name='solar_distance')
]