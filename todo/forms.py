from django.forms import ModelForm
from .models import Todo


# User creation and authentication form were forms by Django, I am now going to make my own form


class Todoform(ModelForm):  # This is going to inherit from ModelForm
    class Meta:  # I think that is a class from Django?
        model = Todo
        fields = ['title', 'memo', 'important']
