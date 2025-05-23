from django.http import HttpResponse
from django.shortcuts import render, loader, redirect
from django.urls import reverse
from .models import User,Admin,Song
#from .forms import ImageUploadForm


def HomePage(request):

    userLogedIn = False

    #if path is empty, send to home page
    if request.path == "/":
        return redirect("/home/")
    

    if request.session.get("loggedUser"):
        userLogedIn = True


    if request.method == "POST":

        if "logout" in request.POST:
            request.session["loggedUser"] = ""
            return redirect("/home/")
        
        if "profile" in request.POST:
            if userLogedIn:

                username = request.session.get("loggedUser")
                userModel = User.objects.get(username=username)
                return redirect(f"/profile/?user={userModel.username}")
            
            else:
                return redirect("/login/")
        
        if "login" in request.POST:
            return redirect("/login/")


    template = loader.get_template("homepage.html")
    context = {"userLogedIn":userLogedIn}
    return HttpResponse(template.render(context, request))


def LogInPage(request):

    userLogedIn = False
    error = ""

    if request.session.get("loggedUser"):
        userLogedIn = True

    if request.method == "POST":

        if "home" in request.POST:
            return redirect("/home/")
        
        if "profile" in request.POST:
            if userLogedIn:
                username = request.session.get("loggedUser")
                userModel = User.objects.get(username=username)
                return redirect(f"/profile/?user={userModel.username}")
            
            else:
                return redirect("/login/")

        #If signup button is pushed
        if "signup" in request.POST:
            return redirect("/signup/")        


        username = request.POST.get("username")
        password = request.POST.get("password")

        #returns the first user that has the name provided
        user = User.objects.filter(username=username).first()

        if user and user.VerifyPassword(password):
            request.session["loggedUser"] = user.username
            return redirect(f"/profile/?user={user.username}")
        
        if username or password:
            error = "Username or Password is incorrect."

    template = loader.get_template("login.html")
    userModel = User.objects.all()
    context = {"users":userModel, "error":error}
    return HttpResponse(template.render(context, request))



def SignUpPage(request):

    error = ""

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        reEnter = request.POST.get("re-enter")

        #check if passwords match
        if not password == reEnter:
            error = "Passwords do not match."

        #check if username is taken
        if User.objects.filter(username=username):
            error = "Username already exists."

        #If there are no errors, proceed
        if "signup" in request.POST and error == "":

            user = User(username=username, email=email, isActive=True)
            user.SetPassword(password)
            user.initialSave()

            return redirect("login")

            
        

    template = loader.get_template("signup.html")
    userModel = User.objects.all()
    context = {"users":userModel, "error":error}
    return HttpResponse(template.render(context, request))



def EditProfilePage(request):

    username = request.session.get("loggedUser")
    userModel = User.objects.get(username=username)

    #If user does not have a session ID, send them to login view
    if username == False or userModel == False:
        return redirect("login")

    username = userModel.username
    userEmail = userModel.email

    error = ""

    if request.method == "POST":

        if "home" in request.POST:
            return redirect("/home/")
        
        if "login" in request.POST:
            return redirect("/login/")
        
        if "profile" in request.POST:
            return redirect(f"/profile/?user={username}")
        
        if "logout" in request.POST:
            request.session["loggedUser"] = ""
            return redirect("/home/")


        if "saveprofile" in request.POST:

            newUsername = request.POST.get("username")
            newEmail = request.POST.get("email")

            if userModel.username != newUsername:

                #check if username is taken
                if User.objects.filter(username=newUsername):
                    error = "Username already exists."
                else:
                    userModel.username = newUsername
                    userModel.save()

            if userModel.email != newEmail:
                userModel.email = newEmail
                userModel.save()

            return redirect(f"/profile/?user={userModel.username}")

        
    template = loader.get_template("editprofile.html")
    context = {"username":userModel.username, "userEmail":userModel.email, "userModel":userModel, "error":error}
    return HttpResponse(template.render(context, request))



def ProfilePage(request):

    username = request.session.get("loggedUser")
    userModel = User.objects.get(username=username)

    #If user does not have a session ID, send them to login view
    if username == False:
        return redirect("login")

    username = userModel.username
    userEmail = userModel.email

    if request.method == "POST":

        if "home" in request.POST:
            return redirect("/home/")
        
        if "login" in request.POST:
            return redirect("/login/")
        
        if "profile" in request.POST:
            return redirect(f"/profile/?user={username}")
        
        if "logout" in request.POST:
            request.session["loggedUser"] = ""
            return redirect("/home/")

        if "editprofile" in request.POST:
            return redirect("edit/?user=" + username)


    template = loader.get_template("profile.html")
    context = {"username":username, "userEmail":userEmail, "userModel":userModel}
    return HttpResponse(template.render(context, request))
    
