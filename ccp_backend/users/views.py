from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import JsonResponse

def connexion_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("accueil")

    return render(request, "connexion.html")


def inscription_view(request):
    if request.method == "POST":
        gender = request.POST.get("gender") or "x"
        last_name = request.POST.get("last_name")
        first_name = request.POST.get("first_name")
        age = request.POST.get("age") or None
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")


        if password1 == password2:
            User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password1
            )
            return redirect("connexion")
        else:
            render(request, "inscription.html", {"error": "Les mots de passe ne correspondent pas"})

    return render(request, "inscription.html")


def accueil_view(request):
    return render(request, 'accueil.html')

def recherche_view(request):
    return render(request, 'recherche.html')

def profil_view(request):
    return render(request, 'profil.html')


def auth_status(request):
    return JsonResponse({
        "isAuthenticated": request.user.is_authenticated
    })

def logout_view(request):
    logout(request)
    return JsonResponse({"success": True})