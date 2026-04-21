from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def connexion_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("accueil")  # à adapter

    return render(request, "connexion.html")


def inscription_view(request):
    if request.method == "POST":
        gender = request.POST.get("gender") or "x"
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        age = request.POST.get("age") or None
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")


        if password1 == password2:
            User.objects.create_user(
                gender=gender,
                surname=surname,
                name=name,
                username=username,
                email=email,
                password=password1
            )
            return redirect("connexion")

    return render(request, "inscription.html")


def accueil_view(request):
    return render(request, 'accueil.html')

def recherche_view(request):
    return render(request, 'recherche.html')

def profil_view(request):
    return render(request, 'profil.html')