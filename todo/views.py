from django.shortcuts import render
# Django forms is  whole topic within itself
from django.contrib.auth.forms import UserCreationForm
# Helps us create user objects really quickly
# This is  the user model we will be using
from django.contrib.auth.models import User

# Create your views here.

''' potential fix: https://stackoverflow.com/questions/48448563/my-password-is-stored-inside-the-email-field-in-django-admin'''


def signupuser(request):
    # I think default is a GET
    if request.method == "GET":
        return render(request, "todo/signupuser.html", {'form': UserCreationForm()})
    else:  # We know it is a post
        if request.POST['password1'] == request.POST['password2']:
            # Create a new user
            user = User.objects.create_user(
                username=request.POST['username'], password=request.POST['password1'])
            user.save()  # This inserts it into the database
        else:
            print('Hello')
            # Tell the user that the passwords did nto match
