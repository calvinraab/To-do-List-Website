from django.contrib import admin
from .models import Todo


# Register your models here.

# This is for if you want to customize what the admin interface looks like for a particular model, we are creating a read only field
class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)


admin.site.register(Todo, TodoAdmin)
