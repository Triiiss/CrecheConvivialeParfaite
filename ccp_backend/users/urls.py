from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path("connexion/", views.connexion_view, name="connexion"),
    path("inscription/", views.inscription_view, name="inscription"),
    path("", views.accueil_view, name="accueil"),
    path("recherche/", views.recherche_view, name="recherche"),
    path("profil/", views.profil_view, name="profil"),
    path("api/auth/", views.auth_status, name="auth_status"),
    path("logout/", views.logout_view, name="logout"),
    path("api/user/", views.get_user),
    path("profil/edit/", views.edit_profile, name="edit_profile"),
]
