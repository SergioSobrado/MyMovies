from django.shortcuts import render
from movies.models import Movie
from movies.models import Person
from movies.models import MovieCredit

# Create your views here.
def index(request):
    movies = Movie.objects.all()
    context = {'movie_list': movies}
    return render(request, './index.html', context)

def movies(request, tmdb_id):
    movies = Movie.objects.get(tmdb_id=tmdb_id)
    credits = MovieCredit.objects.filter(movie=movies.id)
    context = {
        'movie': movies,
        'credits': credits
        } 
    return render(request, './movie.html', context)

def actors(request, name):
    actor = Person.objects.filter(name=name)[0]
    context = {'person': actor}
    return render(request,'./Actors.html',context)
