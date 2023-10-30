from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import User, Family
from shops.models import Product
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class UserForm(forms.ModelForm):
    favorite_products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=FilteredSelectMultiple("Favorite Products", is_stacked=False),
    )

    class Meta:
        model = User
        fields = '__all__'

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

    def __init__(self, *args, **kwargs):
        super(FamilyForm, self).__init__(*args, **kwargs)
        family_instance = kwargs.get('instance')
        if family_instance:
            self.fields['parents'].queryset = User.objects.exclude(id__in=family_instance.kids.all())
            self.fields['kids'].queryset = User.objects.exclude(id__in=family_instance.parents.all())

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'avatar')
        

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data