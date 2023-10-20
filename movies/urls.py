from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('<int:tmdb_id>/', views.movies)
]
