from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import RegistrationForm, UserChangeForm
from django.contrib.auth.decorators import login_required

@login_required
def user_details(request):
    return render(request, 'accounts/user_details.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_details')
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'accounts/edit_profile.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  # Redirect to the home page after successful registration
    else:
        form = RegistrationForm()
        
    return render(request, 'accounts/register.html', {'form': form})