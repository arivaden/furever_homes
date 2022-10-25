from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import CreateAccount, getUserProfile, CreateCOAccount, CreateFOAccount
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
