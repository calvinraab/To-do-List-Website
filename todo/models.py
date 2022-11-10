from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)  # Don't have to fill out the memo
    # Once time is set you can't change it
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    # Doesn't have to be specified by user
    important = models.BooleanField(default=False)

    # This connects the todo to the model (foreign key: one to many relationship)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
