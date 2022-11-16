from django.shortcuts import render, redirect, get_object_or_404
# Django forms is  whole topic within itself
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# Helps us create user objects really quickly
# This is  the user model we will be using
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import Todoform
from .models import Todo
from django.utils import timezone

# Create your views here.

''' potential fix: https://stackoverflow.com/questions/48448563/my-password-is-stored-inside-the-email-field-in-django-admin'''


def home(request):
    return render(request, "todo/home.html")


def signupuser(request):
    # I think default is a GET
    if request.method == "GET":
        return render(request, "todo/signupuser.html", {'form': UserCreationForm()})
    else:  # We know it is a post
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Create a new user
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()  # This inserts it into the database
                # After creating an account this keeps the user logged in.
                login(request, user)
                # And we redirect them to currenttodos
                return redirect('currenttodos')
            # This is the error you get if a username already exists that you are trying.
            except IntegrityError:
                return render(request, "todo/signupuser.html", {'form': UserCreationForm(), 'error': 'That username has already been taken. Please choose a new username.'})

        else:
            return render(request, "todo/signupuser.html", {'form': UserCreationForm(), 'error': 'Passwords did not match'})
            # Tell the user that the passwords did not match


def loginuser(request):
    if request.method == "GET":
        return render(request, "todo/loginuser.html", {'form': AuthenticationForm()})
    else:
        # Don't have to do password1 anymore, see the HTMl on the page for why
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, "todo/loginuser.html", {'form': AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currenttodos')


def logoutuser(request):
    if request.method == 'POST':  # We only want to log people out if it is a post, default in html is going to be a GET that would log us out when we open teh page because Chrome starts running all of the GET functions
        logout(request)
        return redirect('home')


def createtodo(request):
    if request.method == 'GET':
        return render(request, "todo/createtodo.html", {'form': Todoform()})
    else:  # Someone has posted some information to our view
        # We have to get information from our post request to our form
        # Any info it gets it puts into this form
        try:
            form = Todoform(request.POST)
            # create a new Todo object and don't put it in DB yet, we need to specify the user
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, "todo/createtodo.html", {'form': Todoform(), 'error': 'Bad data passed in. Try again.'})


def currenttodos(request):
    # Need to get the todos from database
    # the __isnull is a special django naming convention that can check if a value is null
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos': todos})


def viewtodo(request, todo_pk):
    # We are asking django to lok in the database for a todo that matches that primary key and the users match.
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)

    if request.method == "GET":
        # This form we created from a model. We can pass in an object of that model and it will fill everything out.
        form = Todoform(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form})
    else:  # If it's a post that means the user is 'posting' it.
        try:
            # Adding the instance lets the program know that this exists and we are trying to do an update
            form = Todoform(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form, 'error': 'Bad Info'})


def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == "POST":
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')


def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == "POST":
        todo.delete()
        return redirect('currenttodos')
