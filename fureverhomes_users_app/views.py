from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .forms import CreateAccount, getUserProfile, CreateCOAccount, CreateFOAccount, NewPetProfile
from .models import PetProfile
from .forms import Login


def home(request):
    form = Login(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('dashboard')
    else:
        form = Login()
    return render(request, 'home_page.html', {'form': form})


def error(request):
    return render(request, 'error.html')


def dashboard(request):
    return render(request, 'dashboard.html')

def get_account_type(request):
    if request.method == "POST":
        form = getUserProfile(request.POST)
        if form.is_valid():
            form.save()
        if form.cleaned_data['profile_type'] == 'fo':
            account_form = CreateFOAccount(request.POST)
        else:
            account_form = CreateCOAccount(request.POST)
    else:
        form = getUserProfile()
        account_form = None
    return account_form

def create_account_page(request):
    if request.method == "POST":
        form_to_use = get_account_type(request)
        form = form_to_use
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard')
    else:
        form = CreateAccount()
    return render(request, "registration/create_account_page.html", {"form": form})

"""
def create_pet_profile(request, Owner):
    if request.method == "POST":
        form = NewPetProfile(request.POST)
        if form.is_valid():
            form.cleaned_data['current_owner'] = Owner
            form.save()
    else:
        form = NewPetProfile()
    return render(request, "/my_pets.html" , {"form" : form})

def render_pet_profile(request, pet_id):
    pet = get_object_or_404(PetProfile, id=pet_id)
    return render(request, "/", {"pet": pet})
"""