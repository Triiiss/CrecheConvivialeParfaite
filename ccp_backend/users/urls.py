from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path("connexion/", views.connexion_view, name="connexion"),
    path("inscription/", views.inscription_view, name="inscription"),
]
