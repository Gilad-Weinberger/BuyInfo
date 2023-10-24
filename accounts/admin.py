from django.contrib import admin
from .models import User, Family
from .forms import FamilyForm

class FamilyAdmin(admin.ModelAdmin):
    form = FamilyForm

admin.site.register(User)
admin.site.register(Family, FamilyAdmin)