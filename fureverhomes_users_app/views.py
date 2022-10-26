from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import CreateCOAccount, CreateFOAccount, Login, NewPetProfile
from .models import CurrentOwner, FutureOwner, PetProfile


def home(request):
    form = Login(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('dashboard/dashboard.html')
    else:
        form = Login()
    return render(request, 'home_page.html', {'form': form})


def error(request):
    return render(request, 'error.html')


def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


def select_account_type(request):
    return render(request, "registration/select_account_type.html")


def create_co_account(request):
    form = CreateCOAccount(request.POST)
    if form.is_valid():
        user_email = form.cleaned_data['user_email']
        password = form.cleaned_data['password']
        user_name = form.cleaned_data['user_name']
        user_dob = form.cleaned_data['user_dob']
        user_zip = form.cleaned_data['user_zip']
        CurrentOwner.objects.create_user(email=user_email, password=password, user_name=user_name, user_dob=user_dob, user_zip=user_zip)
        return render(request, 'dashboard/co_dashboard.html')
    return render(request, 'registration/create_co_account.html', {'form': form})


def create_fo_account(request):
    form = CreateFOAccount(request.POST)
    if form.is_valid():
        user_email = form.cleaned_data['user_email']
        password = form.cleaned_data['password']
        user_name = form.cleaned_data['user_name']
        user_dob = form.cleaned_data['user_dob']
        user_zip = form.cleaned_data['user_zip']
        FutureOwner.objects.create_user(email=user_email, password=password, user_name=user_name, user_dob=user_dob,
                              user_zip=user_zip)
        return render(request, 'dashboard/fo_dashboard.html')
    return render(request, 'registration/create_fo_account.html', {'form': form})


def co_dashboard(request):
    return render(request, 'dashboard/co_dashboard')


def fo_dashboard(request):
    return render(request, 'dashboard/fo_dashboard')
