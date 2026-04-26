from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path("", views.accueil_view, name="accueil"),

    path("connexion/", views.connexion_view, name="connexion"),
    path("inscription/", views.inscription_view, name="inscription"),
    path("verification/", views.verify_code, name="verify"),

    path("api/auth/", views.auth_status, name="auth_status"),
    path("logout/", views.logout_view, name="logout"),

    path("api/user/", views.get_user),
    path("profil/", views.profil_view, name="profil"),
    path("profil/edit/", views.edit_profile, name="edit_profile"),
    path("profil/change-password/", views.change_password),
    path('api/all_users/', views.api_all_users, name='api_all_users'),
    path('api/consult_profile/', views.consult_profile, name='api_consult_profile'),
    path('api/consult_object/', views.consult_object, name='api_consult_object'),

    path("information/", views.information_view, name="information"),
    path('api/information/', views.information_api),
    path("objets/", views.objets_view, name="objets"),
    path("api/objets/", views.objets_list, name="api_objets"),
    path("gestion/", views.gestion_view, name="gestion"),
    path('api/objets/update/<int:object_id>/', views.api_update_status, name='api_update_status'),
    path('api/objets/add/', views.api_add_objet, name='api_add_objet'),
    path('api/objets/delete/<int:object_id>/', views.api_delete_objet, name='api_delete_objet'),
    path("statistiques/", views.statistiques_view, name="statistiques"),
    path("statistiques/export/", views.export_csv_view, name="export_csv"),
]
