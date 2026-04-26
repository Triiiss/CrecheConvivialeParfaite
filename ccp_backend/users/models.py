from django.contrib.auth.models import User as AuthUser
from django.db import models


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
    TYPE_CHOICES = [
        ("outsider", "Exterieur"),
        ("enfant", "Enfant"),
        ("parent", "Parent"),
        ("encadrant", "Encadrant"),
        ("directeur", "Directeur"),
    ]
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default="x"
    )
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default="outsider"
    )
    birth_date = models.DateField(null=True, blank=True)
    verification_code = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)

    def __str__(self):
        return f"Profil de {self.user.username}"
    

class Information(models.Model):
    PLACE_CHOICES = [
        ("aile-ouest", "Aile Ouest"),
        ("aile-est", "Aile Est"),
        ("salle-principale", "Salle principale"),
        ("exterieur", "Extérieur"),
    ]

    TARGET_CHOICES = [
        ("parent", "Parent"),
        ("enfant-0-5", "Enfant < 5 ans"),
        ("enfant-5-10", "Enfant 5–10 ans"),
        ("encadrant", "Encadrant"),
    ]

    CATEGORY_CHOICES = [
        ("transport", "Transport"),
        ("divertissement", "Divertissement"),
        ("nourriture", "Nourriture"),
        ("activite", "Activité"),
        ("cours", "Cours"),
    ]

    name = models.CharField(max_length=255)
    place = models.CharField(max_length=50, choices=PLACE_CHOICES)
    target = models.CharField(max_length=50, choices=TARGET_CHOICES)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    date = models.CharField(max_length=20)

    def __str__(self):
        return self.name