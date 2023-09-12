from django.shortcuts import render,redirect
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def home(request):
    return render(request, "index.html")

#creation de compte
def register(request):
    error = False
    message=""
    if request.method =="POST": #la fonction POST pour nouveau inscrit
        name = request.POST.get('fname', None) #recuperation de first name
        lname = request.POST.get('lname', None) #recuperation de last name
        uname = request.POST.get('uname', None) #recuperation de identifiant ou username
        email = request.POST.get('email', None) #recuperation de email
        passwor = request.POST.get('password', None) #recuperation de password champ 1
        repassword = request.POST.get('repassword', None) #recuperation de password champ 2
        
        if validate_email(email)== False:  #verifier si l'email est juste a l'aide de fonction predefinie de Django validate_email
            error = True
        if error==False:
            if passwor!=repassword:  # verifier si les deux mot de passe sont egaux
                error=True
                message="il faut le mot de passe sera identique"
     
            
        user=User.objects.filter(email=email).first()  # recuperation des utilisateur qui ont inscrit avec le meme email
        if user:
            error=True
            message=f"L'utilisateur exist deja avec cet e-mail {email}"
        
        user=User.objects.filter(username=uname).first()  # recuperation des utilisateur qui ont inscrit avec le meme email
        if user:
            error=True
            message=f"L'utilisateur exist deja avec cet identifiant {uname}"   # recuperation des utilisateur qui ont inscrit avec le meme identifiant
        
        if error==False:   #si tous les conditions sont bien respecter
            user=User(    #set objet user de class User avec les parametres necessaire
                first_name=name,
                last_name=lname,
                username=uname,
                email=email,
                
            )
            user.save()   #enregister l'objet avec la fonction de class User save() sans mot de passe
            user.password= passwor
            user.set_password(user.password)
            user.save()  #enregister l'objet avec la fonction de class User save() avec mot de passe
            
            return redirect('signin')   #redirect l'utilisateur vers la page de connexion

    context ={
        'error': error,
        'message':message
    }
    return render(request,"register.html", context)   # rendre l'utilisateur vers la meme page (template) de inscription avec le message de context afficher en haut 


#fonction de connexion
def signin(request):
    if request.method =="POST":
        idenf = request.POST.get('idenf', None)
        passwor = request.POST.get('password', None)
        
        user = User.objects.filter(username=idenf).first()
        if user:
            auth_user = authenticate(username=user.username, password=passwor)  #authentifier l'utilisateur avec les infos saise et verifie en meme temps que sont les deux correct pour un meme enregistrement
            if auth_user:
                login(request, auth_user)  #connection 
                return redirect('profile')  #redirect l'utilisateur vers le profile
                
        
        
    return render(request,"signin.html")


@login_required(login_url='signin') #obligation de connexion pour acceder execute les fonction ci-dessus
def profile(request):
    return render(request,"profile.html")

#deconnexion
def deco(request):
    logout(request)  #la fonction deconnexion
    return redirect('signin')


