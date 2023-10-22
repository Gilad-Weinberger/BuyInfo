from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import User, Family
from django.contrib.auth.forms import UserCreationForm

class FamilyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FamilyForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:            
            self.fields['parents'].queryset = User.objects.exclude(
                family__in=[instance],
                parents=instance
            )
            self.fields['kids'].queryset = User.objects.exclude(
                family__in=[instance],
                kids=instance
            )

    parents = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=FilteredSelectMultiple("User", is_stacked=False),
    )
    kids = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=FilteredSelectMultiple("User", is_stacked=False),
    )

    class Meta:
        model = Family
        fields = '__all__'
