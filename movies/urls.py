from django.urls import path
from django.urls import re_path
from . import views

urlpatterns = [
    path('', views.index),
    path('<int:tmdb_id>/', views.movies),
    path('<str:name>/', views.actors),
]
