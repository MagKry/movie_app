from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse

from .models import Movie, Person, Genre, PersonMovie

# Create your views here.

def movies(request):
    movies = Movie.objects.all().order_by("year")
    sorted = request.session.get("sorted")

    if request.method == "GET":
        if sorted == None:
            sorted = 0
            return render(request, "movies.html", {"movies": movies, "sorted": sorted})
        if sorted == 1:
            movies = Movie.objects.all().order_by("-rating")
            return render(request, "movies.html", {"movies": movies, "sorted": sorted})
        elif sorted == 2:
            movies = Movie.objects.all().order_by("rating")
            return render(request, "movies.html", {"movies": movies, "sorted": sorted})
        elif sorted == 0:
            movies = Movie.objects.all().order_by("year")
            return render(request, "movies.html", {"movies": movies, "sorted": sorted})

    elif request.method == "POST":
        ascending = request.POST.get("ascending")
        descending = request.POST.get("descending")
        default = request.POST.get("default")
        if ascending:
            movies = Movie.objects.all().order_by("rating")
            sorted = 2
            request.session["sorted"] = sorted
            return render(request, "movies.html", {"movies": movies, "sorted": sorted})
        elif descending:
            movies = Movie.objects.all().order_by("-rating")
            sorted = 1
            request.session["sorted"] = sorted
            return render(request, "movies.html", {"movies": movies, "sorted": sorted})
        elif default:
            movies = Movie.objects.all().order_by("year")
            sorted = 0
            request.session["sorted"] = sorted
            return render(request, "movies.html", {"movies": movies, "sorted": sorted})


def movie_details(request, id):
    movie_details = Movie.objects.get(id=id)
    return render(request, "movie_details.html", {"movie": movie_details})

def edit_movie(request, id):
    if request.method == "GET":
        movie = Movie.objects.get(id=id)
        persons = Person.objects.all()
        genres = Genre.objects.all()
        return render(request, "edit_movie.html", {"movie": movie, "persons": persons,\
                                                   "genres": genres})
    elif request.method == "POST":
        title = request.POST.get("title")
        year = int(request.POST.get("year"))
        director = Person.objects.get(id=request.POST.get("director"))
        screenplay = Person.objects.get(id=request.POST.get("screenplay"))
        rating = float(request.POST.get("rating"))
        genre_ids = request.POST.getlist("genre")
        genre = Genre.objects.filter(id__in=genre_ids)

        starring = request.POST.getlist("starring")
        starring_people = Person.objects.filter(id__in=starring)

        movie = Movie.objects.get(id=id)
        movie.title = title
        movie.year = year
        movie.director = director
        movie.screenplay = screenplay
        movie.rating = rating
        movie.genre.set(genre)
        movie.starring.set(starring_people)
        movie.save()

        movies = Movie.objects.all().order_by("id")

        return redirect(reverse("movies"))


def add_movie(request):
    if request.method == "GET":
        persons = Person.objects.all()
        genres = Genre.objects.all()
        return render(request, "add_movie.html", {"persons": persons, "genres": genres})
    elif request.method == "POST":
        title = request.POST.get("title")
        year = int(request.POST.get("year"))
        director = Person.objects.get(id=request.POST.get("director"))
        screenplay = Person.objects.get(id=request.POST.get("screenplay"))
        rating = float(request.POST.get("rating"))
        genre = request.POST.getlist("genre")
        starring = request.POST.getlist("starring")
        starring_people = Person.objects.filter(id__in=starring)

        movie = Movie.objects.create(title=title, year=year, director=director, screenplay=screenplay, rating=rating)
        movie.genre.set(genre)
        movie.starring.set(starring_people)

        movies = Movie.objects.all().order_by("id")

        return redirect(reverse("movies"))


def delete_movie(request, id):
    movie_to_delete = Movie.objects.get(id=id)
    movie_to_delete.delete()
    return HttpResponse(f"Movie with id:{id} deleted.")



def search_movie(request):
    if request.method == "GET":
        return render(request, "search_movie.html")
    elif request.method == "POST":
        title = request.POST.get("title")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        year_from = request.POST.get("year_from")
        year_to = request.POST.get("year_to")
        selected_genres = request.POST.getlist("genre")

        try:
            rating_from = float(request.POST.get("rating_from"))
            rating_to = float(request.POST.get("rating_to"))
        except ValueError:
            rating_from = None
            rating_to = None

        if (title == "" and
            first_name == "" and
            last_name == "" and
            year_from == "" and
            year_to == "" and
            selected_genres == [] and
            rating_to is None and
            rating_from is None):
            searched_movies = Movie.objects.all()
            return render(request, "search_results.html", {"searched_movies": searched_movies})

        elif title != "":
            searched_movies = Movie.objects.filter(title=title)
            return render(request, "search_results.html", {"searched_movies": searched_movies})

        elif first_name != "":
            persons = Person.objects.filter(first_name=first_name)
            searched_movies = Movie.objects.filter(Q(director__in=persons) | Q(screenplay__in=persons) | Q(starring__in=persons)).distinct() #spr starring po dodaniu aktorów
            return render(request, "search_results.html", {"searched_movies": searched_movies})

        elif last_name != "":
            persons = Person.objects.filter(last_name=last_name)
            searched_movies = Movie.objects.filter(Q(director__in=persons) | Q(screenplay__in=persons) | Q(starring__in=persons)) #spr starring po dodaniu aktorów
            return render(request, "search_results.html", {"persons": persons, "searched_movies": searched_movies})

        elif year_from and year_to != "":
            movie = Movie.objects.all()
            searched_movies = Movie.objects.filter(year__gte=year_from).filter(year__lte=year_to)
            return render(request, "search_results.html", {"searched_movies": searched_movies, "movie": movie})

        elif rating_from and rating_to is not None:
            movie = Movie.objects.all()
            searched_movies = Movie.objects.filter(rating__gte=rating_from).filter(rating__lte=rating_to)
            return render(request, "search_results.html", {"searched_movies": searched_movies, "movie": movie})

        elif selected_genres != "":
            movie = Movie.objects.all()
            searched_movies = []

            for selected_genre in selected_genres:
                searched_movie = Movie.objects.filter(genre__name__icontains=selected_genre)
                searched_movies.extend(searched_movie)

            return render(request, "search_results.html", {"searched_movies": searched_movies, "movie": movie})

        else:
            return HttpResponse("There are no movies meeting this search criteria.")


def persons(request):
    persons = Person.objects.all()
    return render(request, "persons.html", {"persons": persons})


def edit_person(request, id):
    if request.method == "GET":
        person_details = Person.objects.get(id=id)
        return render(request, "edit_person.html", {"person": person_details})
    elif request.method == "POST":
        new_first_name = request.POST.get("first_name")
        new_last_name = request.POST.get("last_name")
        new_person_details = Person.objects.filter(id=id).update(first_name=new_first_name, last_name=new_last_name)
        return HttpResponse(f"{id}{new_first_name}{new_last_name}")


def add_person(request):
    if request.method == "GET":
        return render(request, "add_person.html")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        new_person = Person.objects.create(first_name=first_name, last_name=last_name)
        persons = Person.objects.all()
        return render(request, "persons.html", {"persons": persons})

def delete_person(request, id):
    person_to_delete = Person.objects.get(id=id)
    person_to_delete.delete()
    return HttpResponse (f"Person with id: {id} deleted.")