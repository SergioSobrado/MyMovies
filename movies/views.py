from django.shortcuts import render
from movies.models import Movie

# Create your views here.
def index(request):
    movies = Movie.objects.all()
    context = {'movie_list': movies}
    return render(request, './index.html', context)

def movies(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    context = {'movie': movie}
    return render(request, './movie.html', context)