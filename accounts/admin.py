from django.contrib import admin
from .models import User, Family
from .forms import UserForm, FamilyForm

class UserAdmin(admin.ModelAdmin):
    form = UserForm

class FamilyAdmin(admin.ModelAdmin):
    form = FamilyForm

admin.site.register(User, UserAdmin)
admin.site.register(Family, FamilyAdmin)