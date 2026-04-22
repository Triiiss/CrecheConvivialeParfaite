from django.db import models
from django.contrib.auth.models import User as AuthUser


class User(models.Model):
    genre = models.CharField(max_length=10, blank=True)
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_naissance = models.DateField(null=True, blank=True)
    login = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.login


class Profile(models.Model):
    GENDER_CHOICES = [
        ("mr", "Monsieur"),
        ("mme", "Madame"),
        ("x", "Autre"),
    ]
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default="x"
    )
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Profil de {self.user.username}"