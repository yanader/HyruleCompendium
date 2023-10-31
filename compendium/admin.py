from django.contrib import admin
from .models import User, Completion, Todo

# Register your models here.
admin.site.register(User)
admin.site.register(Completion)
admin.site.register(Todo)