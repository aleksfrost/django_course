from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from .models import User, Note
from django.shortcuts import render, redirect


# Create your views here.

def home_page(request):
    return render(request, "index.html")


def reg_page(request):
    if request.method == "GET":
        return render(request, "reg_page.html")
    else:
        data = request.POST
        username = data.get("username")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        password1, password2 = data.get("password1"), data.get("password2")
        if username is None:
            message = "username not entered"
            context = {'status': message}
            return render(request, "reg_page.html", context)
        elif email is None:
            message = "email not entered"
            context = {'status': message}
            return render(request, "reg_page.html", context)
        elif password1 is None or password2 is None:
            message = "confirm password"
            context = {'status': message}
            return render(request, "reg_page.html", context)
        elif password1 != password2:
            message = "passwords not match"
            context = {'status': message}
            return render(request, "reg_page.html", context)
        else:
            try:
                new_user = User(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    is_active=True
                )
                new_user.is_staff = True
                new_user.set_password(password1)
                # password MUST BE SET! to be hashed, or authenticate'ion will not pass
                new_user.save()
                message = "success, registration complete"
                context = {'status': message}
                return render(request, "reg_page.html", context)
            except:
                message = f"Fail, User {username} already exists"
                context = {'status': message}
                return render(request, "reg_page.html", context)


def login_page(request):
    if request.method == "GET":
        message = 'You should login'
        context = {"message": message}
        return render(request, "login_page.html", context)
    else:
        data = request.POST
        try:
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is None:
                message = "The user with such name not found"
                context = {'message': message}
                return render(request, "login_page.html", context)
            login(request, user)
            message = "Login successfully"
            context = {'message': message}
            return render(request, "login_page.html", context)
        except KeyError:
            message = "All fields must be filled"
            context = {'message': message}
            return render(request, "login_page.html", context)


def logout_page(request):
    if request.user.is_authenticated:
        message = f"User {request.user.username} is logged out"
        logout(request)
        context = {"status": message}
        return render(request, 'logout_page.html', context)
    else:
        message = f"You are not logged in, would you like to?"
        context = {"status": message}
        return render(request, 'logout_page.html', context)


def show_notes_page(request):
    if request.user.is_authenticated:
        user = request.user.id
    else:
        return render(request, "login_page.html")
    query = Note.objects.filter(user=user).all()
    notes = [note.content for note in query]
    context = {'notes': notes}
    return render(request, "notes.html", context)


def add_note_page(request):
    if request.method == "GET":
        message = 'Enter your note'
        context = {"context": message}
        return render(request, "add_note.html", context)
    else:
        data = request.POST
        new_note = Note(
            content=data["note"],
            user_id=request.user.id
        )
        new_note.save()
        message = "Note added"
        context = {"message": message}
        return render(request, "add_note.html", context)
