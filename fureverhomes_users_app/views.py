from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import CreateCOAccount, CreateFOAccount, Login, DogForm, CatForm, PetType
from .models import CurrentOwner, FutureOwner, PetProfile, Dog, Cat


def home(request):
    form = Login(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            dashboard(request) #return HttpResponseRedirect('dashboard/dashboard.html')
    else:
        form = Login()
    return render(request, 'home_page.html', {'form': form})


def error(request):
    return render(request, 'error.html')


def dashboard(request):
    if not request.user.is_anonymous:
        id = request.user.user_id
        isCo = True

        try:
            co = CurrentOwner.objects.get(user_id=id)
        except CurrentOwner.DoesNotExist:
            isCo = False

        if isCo:
            return co_dashboard(request) #render(request, 'dashboard/co_dashboard.html')
        else:
            return fo_dashboard(request)#render(request, 'dashboard/fo_dashboard.html')
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
    owner = CurrentOwner.objects.get(user_id=request.user.user_id)
    pets = owner.view_my_pets()
    context = {'pets': pets}
    return render(request, 'dashboard/co_dashboard.html', context)


def fo_dashboard(request):
    return render(request, 'dashboard/fo_dashboard')


def select_pet_type(request):
    # commenting this out until I can get it to work so we can dynamically load pet form into single html file
    #form = PetType(request.POST)
    return render(request, 'pets/select_pet_type.html')


def create_cat_profile(request):
    form = CatForm(request.POST, request.FILES)
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
        owner = CurrentOwner.objects.get(user_id=request.user.user_id)
        declawed = form.cleaned_data['is_declawed']
        Cat.objects.create_pet_profile(owner, pet_name, description=description, profile_pic=profile_pic, age=age,
                                       sex=sex, size=size, good_w_kids=good_w_kids,
                                       spayed_or_neutered=spayed_or_neutered, rehoming_reason=rehoming_reason,
                                       is_declawed=declawed)
        return redirect('co_dashboard') #return render(request, 'dashboard/co_dashboard.html')
    return render(request, 'pets/create_cat_profile.html', {'form': form})


def code_of_conduct(request):
    return render(request, 'registration/code_of_conduct.html')


def create_dog_profile(request):
    form = DogForm(request.POST, request.FILES)
    if form.is_valid():
        #form.save()
        data = form.cleaned_data
        pet_name = data['pet_name']
        description = data['description']
        profile_pic = data['profile_pic']
        age = data['age']
        sex = data['sex']
        size = data['size']
        good_w_kids = data['good_w_kids']
        spayed_or_neutered = data['spayed_or_neutered']
        rehoming_reason = data['rehoming_reason']
        owner = CurrentOwner.objects.get(user_id=request.user.user_id)
        breed = form.cleaned_data['breed']
        Dog.objects.create_pet_profile(owner, pet_name, description=description, profile_pic=profile_pic, age=age, sex=sex, size=size, good_w_kids=good_w_kids, spayed_or_neutered=spayed_or_neutered, rehoming_reason=rehoming_reason, breed=breed)
        return redirect('co_dashboard') #return render(request, 'dashboard/co_dashboard.html')
    return render(request, 'pets/create_dog_profile.html', {'form': form})


def pet_profile(request, pet_profile_id):
    pet_model = PetProfile.objects.get(pet_profile_id=pet_profile_id)
    editor = False
    id = request.user.user_id
    if id == pet_model.current_owner.user_id:
        editor = True
    fixed = pet_model.spayed_or_neutered
    good_w_kids = pet_model.good_w_kids
    age_choices = {0:'Young: 0-1 Years', 1:"Adult: 1-6 Years", 2:"Senior: 6+ Years"}
    size_choices = {1:"Small", 2:"Medium", 3:"Large"}
    sex_choices = {'M':'Male', 'F':'Female', 'U':'Unknown'}
    y = "Yes"
    n = "No"
    spayed_neutered = n
    kids = n
    if fixed:
        spayed_neutered = y
    if good_w_kids:
        kids = y
    pet = {
        "pet_profile_id" : pet_model.pet_profile_id,
        "pet_name" : pet_model.pet_name,
        "size" : size_choices.get(pet_model.size),
        "sex" : sex_choices.get(pet_model.sex),
            "spayed_or_neutered" : spayed_neutered,
           "good_w_kids" : kids,
           "age": age_choices.get(pet_model.age),
           "profile_pic": pet_model.profile_pic,
           "description": pet_model.description,
            "rehoming_reason" : pet_model.rehoming_reason

    }
    return render(request, 'pets/pet_profile.html', {'pet': pet, 'editor':editor})

def edit_pet_profile(request, pet_profile_id):
    pet = PetProfile.objects.get(pet_profile_id = pet_profile_id)

    pet.edit_pet_profile()
    return(request, )

def delete_pet_profile(self, pet_profile_id):
    pet = PetProfile.objects.get(pet_profile_id = pet_profile_id)
    pet.delete()
    return redirect('co_dashboard')

def mark_as_adopted(pet_profile_id):
    pet = PetProfile.objects.get(pet_profile_id=pet_profile_id)
    pet.mark_as_adopted()
    return redirect('co_dashboard')