from django.contrib import admin
from django.urls import path, include
from .views import movies, movie_details, persons, edit_person, add_person, edit_movie, add_movie, search_movie, \
    delete_movie, delete_person

urlpatterns = [
    path("movies/", movies, name="movies"),
    path("movie_details/<int:id>/", movie_details, name="movie_details"),
    path("persons/", persons, name="persons"),
    path("edit-person/<int:id>/", edit_person, name="edit_person"),
    path("add-person/", add_person, name="add_person"),
    path("edit-movie/<int:id>/", edit_movie, name="edit_movie"),
    path("add-movie/", add_movie, name="add_movie"),
    path('search-movie/', search_movie, name="search_movie"),
    path("del-movie/<int:id>/", delete_movie, name="delete_movie"),
    path("del-person/<int:id>/", delete_person, name="delete_person"),
]