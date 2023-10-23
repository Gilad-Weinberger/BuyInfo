from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import User
from .models import Family

class FamilyForm(forms.ModelForm):
    parents = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=FilteredSelectMultiple("Parents", is_stacked=False),
    )
    kids = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=FilteredSelectMultiple("Kids", is_stacked=False),
    )

    class Meta:
        model = Family
        fields = '__all__'
