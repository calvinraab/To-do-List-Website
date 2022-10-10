from django.shortcuts import render, redirect
# Django forms is  whole topic within itself
from django.contrib.auth.forms import UserCreationForm
# Helps us create user objects really quickly
# This is  the user model we will be using
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login

# Create your views here.

''' potential fix: https://stackoverflow.com/questions/48448563/my-password-is-stored-inside-the-email-field-in-django-admin'''


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
            # This is the error you get if a username already exists that you are trying.
                # After creating an account this keeps the user logged in.
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, "todo/signupuser.html", {'form': UserCreationForm(), 'error': 'That username has already been taken. Please choose a new username.'})

        else:
            return render(request, "todo/signupuser.html", {'form': UserCreationForm(), 'error': 'Passwords did not match'})
            # Tell the user that the passwords did not match


def currenttodos(request):
    return render(request, 'todo/currenttodos.html')
