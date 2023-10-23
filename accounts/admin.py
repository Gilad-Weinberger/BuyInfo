from django.contrib import admin
from django.contrib.auth.models import User
from .models import Family
from .forms import FamilyForm

class FamilyAdmin(admin.ModelAdmin):
    form = FamilyForm

admin.site.register(Family, FamilyAdmin)