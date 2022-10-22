from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import CreateAccount
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


def create_account_page(request):
    if request.method == "POST":
        form = CreateAccount(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard')
    else:
        form = CreateAccount()
    return render(request, "registration/create_account_page.html", {"form": form})
