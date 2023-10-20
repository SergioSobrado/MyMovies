from django.shortcuts import render
from movies.models import Movie
from movies.models import Person

# Create your views here.
def index(request):
    movies = Movie.objects.all()
    context = {'movie_list': movies}
    return render(request, './index.html', context)

def movies(request, tmdb_id):
    movie = Movie.objects.get(tmdb_id=tmdb_id)
    context = {'movie': movie}
    return render(request, './movie.html', context)

def actors(request, name):
    actor = Person.objects.get(name=name)
    context = {'person': actor}
    return render(request,'./Actors.html',context)