from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash
from .models import Information
from .models import Profile
from .models import Objet
import random


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
        type = request.POST.get("type")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if User.objects.filter(username=username).exists():
            return render(request, "inscription.html", {
                "error": "Ce nom d'utilisateur est déjà pris"
            })
        elif User.objects.filter(email=email).exists():
            return render(request, "inscription.html", {
                "error": "Cet email est déjà pris"
            })
        elif password1 != password2:
            return render(request, "inscription.html", {
                "error": "Les mots de passe ne correspondent pas"
            })
        elif type == "outsider":
            return render(request, "inscription.html", {
                "error": "La crèche n'accepte pas de personnes extérieures"
            })
        else:
            code = str(random.randint(100000, 999999))
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password1
            )
            Profile.objects.create(user=user, points=1, gender=gender,birth_date=birth_date,type=type, verification_code=code)
            send_mail(
                subject="Votre code de validation",
                message=f"Votre code est : {code}",
                from_email="no-reply@tonsite.com",
                recipient_list=[email],
            )
            request.session["verify_user_id"] = user.id
            return redirect("verify")

    return render(request, "inscription.html")


def verify_code(request):
    MAX_ATTEMPTS = 5
    user_id = request.session.get("verify_user_id")

    if not user_id:
        return redirect("inscription")

    try:
        user = User.objects.get(id=user_id)
        profile = Profile.objects.get(user=user)
    except (User.DoesNotExist, Profile.DoesNotExist):
        return redirect("inscription")

    if request.method == "POST":
        code = request.POST.get("code")

        # ✅ Code correct
        if profile.verification_code == code:
            profile.is_verified = True
            profile.verification_code = None
            profile.attempts = 0
            profile.save()

            user.is_active = True
            user.save()

            del request.session["verify_user_id"]

            return redirect("connexion")

        else:
            profile.attempts += 1
            if profile.attempts >= MAX_ATTEMPTS:
                user.delete()
                request.session.pop("verify_user_id", None)

                return render(request, "verify.html", {
                    "error": "Trop de tentatives. Compte supprimé."
                })

            profile.save()

            return render(request, "verify.html", {
                "error": f"Code incorrect ({profile.attempts}/{MAX_ATTEMPTS})"
            })

    return render(request, "verify.html")


def accueil_view(request):
    return render(request, 'accueil.html')


def information_view(request):
   return render(request, 'information.html')


def information_api(request):
    items = list(Information.objects.values())
    return JsonResponse(items, safe=False)


def profil_view(request):
    if not request.user.is_authenticated:       #Si l'utilisateur est connecté, il est renvoyé vers l'accueil
        return redirect("accueil")

    profile, _ = Profile.objects.get_or_create(user=request.user)
    points = profile.points
    rank = get_rank(points)

    return render(request, 'profil.html', {
        'points': points,
        'rank' : rank
    })


def objets_view(request):
    if not request.user.is_authenticated:       #Si l'utilisateur est connecté, il est renvoyé vers l'accueil
        return redirect("accueil")
    return render(request, 'recherche_objets.html')


def objets_list(request):
    objets = list(Objet.objects.values())
    return JsonResponse(objets, safe=False)


def gestion_view(request):
    if not request.user.is_authenticated or request.user.profile.points < 500:       #Si l'utilisateur est connecté, il est renvoyé vers l'accueil
        return redirect("accueil")
    return render(request, 'gestion.html')


def auth_status(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            "isAuthenticated": False,
            "rank": None,
            "points": 0
        })

    profile, _ = Profile.objects.get_or_create(user=request.user)

    return JsonResponse({
        "isAuthenticated": True,
        "rank": get_rank(profile.points),
        "points": profile.points
    })


def logout_view(request):
    logout(request)
    return JsonResponse({"success": True})

def edit_profile(request):
  if not request.user.is_authenticated:
    return redirect("accueil")

  profile = Profile.objects.get(user=request.user)

  if request.method == "POST":
    password = request.POST.get("confirm")

    if not request.user.check_password(password):
      return render(request, "profil.html", {
        "error": "Mot de passe incorrect",
        "active_tab": "settings"
      })

    request.user.first_name = request.POST.get("first_name") or request.user.first_name
    request.user.last_name = request.POST.get("last_name") or request.user.last_name
    request.user.email = request.POST.get("email") or request.user.email
    profile.gender = request.POST.get("gender") or profile.gender
    profile.birth_date = request.POST.get("birth_date") or profile.birth_date

    profile.points += 2

    request.user.save()
    profile.save()

    return render(request, "profil.html", {
        "message": "Informations modifiées avec succès"
      })

  return redirect("profil")

def change_password(request):
  if not request.user.is_authenticated:
    return redirect("accueil")

  if request.method == "POST":
    old_password = request.POST.get("old_password")
    new_password = request.POST.get("new_password")
    confirm_password = request.POST.get("confirm_password")

    if not request.user.check_password(old_password):
      return render(request, "profil.html", {
        "ps_error": "Ancien mot de passe incorrect",
        "active_tab": "settings"
      })

    if new_password != confirm_password:
      return render(request, "profil.html", {
        "password_error": "Les mots de passe ne correspondent pas",
        "active_tab": "settings"
      })

    request.user.set_password(new_password)
    request.user.save()

    update_session_auth_hash(request, request.user)

    return render(request, "profil.html", {
      "password_message": "Votre mot de passe a bien été modifié",
      "active_tab": "settings"
    })

  return redirect("profil")

#Getter
def get_user(request):
  if not request.user.is_authenticated:
    return JsonResponse({"error": "not authenticated"}, status=401)

  profile, _ = Profile.objects.get_or_create(user=request.user)

  return JsonResponse({
    "username": request.user.username,
    "last_name": request.user.last_name,
    "first_name": request.user.first_name,
    "mail": request.user.email,
    "birthdate": profile.birth_date,
    "gender": profile.gender,
    "points": profile.points,
    "type" : profile.type,
    "rank" : get_rank(profile.points),
  })

#Fonction qui retourne le rang de l'utilisateur
def get_rank(points):
  if points >= 1000:
    return "Expert"
  elif points >= 500:
    return "Avancé"
  elif points >= 100:
    return "Intermédiaire"
  return "Débutant"


#Fonction qui renvoie la liste des utilisateurs au format JSON
def api_all_users(request):
    profiles = Profile.objects.select_related('user').all() #select_related agit comme une jointure
    #pour que django ne refasse pas 10 requetes pour les user

    data = []
    for p in profiles:
        data.append({
            "username": p.user.username,
            "last_name": p.user.last_name,
            "first_name": p.user.first_name,
            "mail": p.user.email,
            "role": p.type,
            "gender": p.gender,
            "birthdate": str(p.birth_date),
            "pfp": "/static/img/anonymous.png"
        })

    return JsonResponse(data, safe=False)


def consult_profile(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "not authenticated"}, status=401)

    profile, _ = Profile.objects.get_or_create(user=request.user)

    profile.points += 10

    profile.save()

    return JsonResponse({"success": True, "new_points": profile.points})


def consult_object(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "not authenticated"}, status=401)

    profile, _ = Profile.objects.get_or_create(user=request.user)

    profile.points += 5

    profile.save()

    return JsonResponse({"success": True, "new_points": profile.points})
