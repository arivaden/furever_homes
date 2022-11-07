from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import CreateCOAccount, CreateFOAccount, Login, DogForm, CatForm, PetType
from .models import CurrentOwner, FutureOwner, PetProfile, Dog, Cat


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
    usertype = type(request.user)
    if usertype is CurrentOwner:
        return render(request, 'dashboard/co_dashboard.html')
    elif usertype is FutureOwner:
        return render(request, 'dashboard/fo_dashboard.html')
    else:
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


def select_pet_type(request):
    # commenting this out until I can get it to work so we can dynamically load pet form into single html file
    #form = PetType(request.POST)
    return render(request, 'pets/select_pet_type.html')

def create_cat_profile(request):
    form = CatForm(request.POST)
    if form.is_valid():
        pet_name = form.cleaned_data['pet_name']
        description = form.cleaned_data['description']
        profile_pic = form.cleaned_data['profile_pic']
        age = form.cleaned_data['age']
        sex = form.cleaned_data['sex']
        size = form.cleaned_data['size']
        good_w_kids = form.cleaned_data['good_w_kids']
        spayed_or_neutered = form.cleaned_data['spayed_or_neutered']
        rehoming_reason = form.cleaned_data['rehoming_reason']
        owner = request.user.user_id
        declawed = form.cleaned_data['is_declawed']
        Cat.objects.create_pet_profile(owner, pet_name, description=description, profile_pic=profile_pic, age=age,
                                       sex=sex, size=size, good_w_kids=good_w_kids,
                                       spayed_or_neutered=spayed_or_neutered, rehoming_reason=rehoming_reason,
                                       is_declawed=declawed)
        return render(request, 'dashboard/co_dashboard.html')
    return render(request, 'pets/create_cat_profile.html', {'form': form})

def create_dog_profile(request):
    form = DogForm(request.POST)
    if form.is_valid():
        pet_name = form.cleaned_data['pet_name']
        description = form.cleaned_data['description']
        profile_pic = form.cleaned_data['profile_pic']
        age = form.cleaned_data['age']
        sex = form.cleaned_data['sex']
        size = form.cleaned_data['size']
        good_w_kids = form.cleaned_data['good_w_kids']
        spayed_or_neutered = form.cleaned_data['spayed_or_neutered']
        rehoming_reason = form.cleaned_data['rehoming_reason']
        owner = request.user.user_id
        breed = form.cleaned_data['breed']
        Dog.objects.create_pet_profile(owner, pet_name, description=description, profile_pic=profile_pic, age=age, sex=sex, size=size, good_w_kids=good_w_kids, spayed_or_neutered=spayed_or_neutered, rehoming_reason=rehoming_reason, breed=breed)
        return render(request, 'dashboard/co_dashboard.html')
    return render(request, 'pets/create_dog_profile.html', {'form': form})
