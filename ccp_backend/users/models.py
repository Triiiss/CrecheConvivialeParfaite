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
