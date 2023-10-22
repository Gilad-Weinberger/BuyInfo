from django.contrib import admin
from .models import User
from .forms import UserForm

class UserAdmin(admin.ModelAdmin):
    form = UserForm

admin.site.register(User, UserAdmin)