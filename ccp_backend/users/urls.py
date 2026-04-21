from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path("connexion/", views.connexion_view, name="connexion"),
    path("inscription/", views.inscription_view, name="inscription"),
    path("accueil/", views.accueil_view, name="accueil"),
    path("recherche/", views.recherche_view, name="recherche"),
    path("profil/", views.profil_view, name="profil"),
]
