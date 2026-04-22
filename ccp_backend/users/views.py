from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import JsonResponse
from .models import Profile


def connexion_view(request):
    if request.user.is_authenticated:       #Si l'utilisateur est connecté, il est renvoyé vers l'accueil
        return redirect("accueil")
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, "connexion.html", {
                "error": "L'identifiant ou le mot de passe est incorrect"
            })
        login(request, user)
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.points += 5
        profile.save()

        return redirect("accueil")

    return render(request, "connexion.html")


def inscription_view(request):
    if request.user.is_authenticated:       #Si l'utilisateur est connecté, il est renvoyé vers l'accueil
        return redirect("accueil")
    
    if request.method == "POST":
        gender = request.POST.get("gender") or "x"
        last_name = request.POST.get("last_name")
        first_name = request.POST.get("first_name")
        birth_date = request.POST.get("birth_date") or None
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if User.objects.filter(username=username).exists():
            return render(request, "inscription.html", {
                "error": "Ce nom d'utilisateur est déjà pris"
            })
        elif password1 != password2:
            return render(request, "inscription.html", {
                "error": "Les mots de passe ne correspondent pas"
            })
        else:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password1
            )
            Profile.objects.create(user=user, points=10)
            return redirect("connexion")

    return render(request, "inscription.html")


def accueil_view(request):
    return render(request, 'accueil.html')


def recherche_view(request):
    return render(request, 'recherche.html')


def profil_view(request):
    if not request.user.is_authenticated:       #Si l'utilisateur est connecté, il est renvoyé vers l'accueil
        return redirect("accueil")
    points = 0
    niveau = 0
    if request.user.is_authenticated:
        profile, created = Profile.objects.get_or_create(user=request.user)
        points = profile.points
        niveau = points // 50
    return render(request, 'profil.html', {
        'points': points,
        'niveau': niveau,
    })


def auth_status(request):
    return JsonResponse({
        "isAuthenticated": request.user.is_authenticated
    })


def logout_view(request):
    logout(request)
    return JsonResponse({"success": True})