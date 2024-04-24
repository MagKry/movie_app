from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)


    def __str__(self):
        return f"{self.person}"

    def __str__(self):
        name = f"{self.first_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"

class Genre(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return f"self.name"


class Movie(models.Model):
    title = models.CharField(max_length=128)
    director = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="directed_movies")
    screenplay = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="screenplayed_movies")
    starring = models.ManyToManyField(Person, related_name="starring", through="PersonMovie")
    year = models.IntegerField()
    rating = models.FloatField(validators=[MinValueValidator(limit_value=1.0),
                                           MaxValueValidator(limit_value=10.0)], default=0.0)
    genre = models.ManyToManyField(Genre)


    def __str__(self):
        return f"{self.title}, Directed by: {self.director}, Screenplayed by: {self.screenplay}, Starring: {', '.join(str(person) for person in self.starring.all())}, Year: {self.year}, Rating: {self.rating}, Genre: {', '.join(str(genre) for genre in self.genre.all())}"


class PersonMovie(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.CharField(max_length=128, null=True, blank=True)


    def __str__(self):
        return f"self.person"
