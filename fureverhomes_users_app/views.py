from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import CreateCOAccount, CreateFOAccount, Login, DogForm, CatForm, GetPreferences, MessageForm
from .models import CurrentOwner, FutureOwner, PetProfile, Dog, Cat, Message, User
import datetime


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
            return co_dashboard(request)
        else:
            return fo_dashboard(request)
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
    new_messages = owner.getNewMessages()
    pets = owner.view_my_pets()
    context = {'pets': pets, 'new_messages': len(new_messages)}
    return render(request, 'dashboard/co_dashboard.html', context)


def fo_dashboard(request):
    adopter = FutureOwner.objects.get(user_id=request.user.user_id)
    new_messages = adopter.getNewMessages()
    pref_form = GetPreferences(request.POST)
    if pref_form.is_valid():
        size = pref_form.cleaned_data['size_pref']
        type = pref_form.cleaned_data['type_pref']
        age = pref_form.cleaned_data['age_pref']
        kids = pref_form.cleaned_data['kids_pref']
        fixed = pref_form.cleaned_data['fixed_pref']
        sex = pref_form.cleaned_data['sex_pref']
        adopter.edit_preferences(type, size, age, sex, kids, fixed)
        pets_in_area = adopter.find_pets()
        return render(request, 'dashboard/fo_dashboard.html', {'pref_form': pref_form, 'pet_pool':pets_in_area, 'new_messages' :new_messages})
    return render(request, 'dashboard/fo_dashboard.html', {'pref_form': pref_form, 'new_messages':new_messages})


def fo_liked_pets(request):
    adopter = FutureOwner.objects.get(user_id=request.user.user_id)
    interested_pets = adopter.view_liked_pets()
    return render(request, 'pets/fo_liked_pets.html', {'liked_pets':interested_pets})


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
    adopter = True
    id = request.user.user_id
    if id == pet_model.current_owner.user_id:
        editor = True
        adopter = False
    else:
        try:
            fo = FutureOwner.objects.get(user_id=id)
        except FutureOwner.DoesNotExist:
            adopter = False
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
        "rehoming_reason" : pet_model.rehoming_reason,
        "is_adopted": pet_model.is_adopted,
        "interested_users": pet_model.interested_users
    }
    if adopter:
        fo = FutureOwner.objects.get(user_id=id)
    else:
        fo = None
    return render(request, 'pets/pet_profile.html', {'pet': pet, 'editor':editor, 'adopter':adopter, 'fo': fo})


def edit_pet_profile(request, pet_profile_id):
    pet = PetProfile.objects.get(pet_profile_id = pet_profile_id)
    id = pet_profile_id
    isCat = True
    try:
        pet = Cat.objects.get(pet_profile_id=id)
    except pet.DoesNotExist:
        isCat = False

    if isCat:
        form = CatForm(request.POST, request.FILES)
        return render(request, 'pets/edit_pet_profile.html', {'form': form})
    else:
        form = DogForm(request.POST, request.FILES)
        return render(request, 'pets/edit_pet_profile.html', {'form': form})


def delete_pet_profile(self, pet_profile_id):
    pet = PetProfile.objects.get(pet_profile_id = pet_profile_id)
    pet.delete()
    return redirect('co_dashboard')

'''
def mark_as_adopted(self, pet_profile_id):
    pet = PetProfile.objects.get(pet_profile_id=pet_profile_id)
    pet.mark_as_adopted()
    return redirect('co_dashboard')
'''


def update_adoption_status(self, pet_profile_id):
    pet = PetProfile.objects.get(pet_profile_id=pet_profile_id)
    pet.update_adoption_status()
    return redirect('co_dashboard')

'''
def mark_as_interested(request, pet_profile_id):
    pet = PetProfile.objects.get(pet_profile_id=pet_profile_id)
    adopter = FutureOwner.objects.get(user_id=request.user.user_id)
    pet.mark_as_interested(adopter)
    return redirect('fo_liked_pets')
'''


  # render(request, 'pets/pet_profile.html')
def update_interest_status(request, pet_profile_id):
    pet = PetProfile.objects.get(pet_profile_id=pet_profile_id)
    adopter = FutureOwner.objects.get(user_id=request.user.user_id)
    pet.update_interest_status(adopter)
    return redirect('fo_liked_pets')


def inbox(request):
    id = request.user.user_id
    is_co = True
    try:
        co = CurrentOwner.objects.get(user_id=id)
    except CurrentOwner.DoesNotExist:
        is_co = False
    if is_co:
        #returns two tiered list
        owner = CurrentOwner.objects.get(user_id=id)
        #contactable_users = owner.get_contactable_adopters()
        contacts = []
        #pets to iterate through
        pets = owner.view_my_pets()
        #determine which pets have interested users
        pets_w_users = []
        for i in pets:
            #cast to list the interested users
            interest_cast_list = list(i.interested_users.all())
            #if list of interested users is not empty
            if interest_cast_list:
                pets_w_users.append(i)
                for j in interest_cast_list:
                    contacts.append(j)
        new_messages = co.getNewMessagesDict()
    else:
        #returns only owner objects
        adopter = FutureOwner.objects.get(user_id= id)
        pets_w_users = None
        contacts = adopter.get_contactable_owners()
        new_messages = adopter.getNewMessagesDict()
        #new_message_senders = new_messages.keys()
    return render(request, 'messaging/inbox.html', {'is_co': is_co, 'contacts': contacts,
                                                    'pets_w_users': pets_w_users, 'new_messages_dict':new_messages,
                                                    'new_message_senders': new_messages.keys() })


def direct_message(request, recipient_id):
    sender_id = request.user.user_id
    # display previous message history ordered by date
    sender = User.objects.get(user_id = sender_id)
    recipient = User.objects.get(user_id=recipient_id)
    messages = sender.getMessageHistory(recipient_id)
    # once we open the conversation, mark all the messages as read, since the user has seen them
    for msg in messages:
        msg.mark_read()
    # should be able to submit a message as a form, and when its created, save DT
    message_form = MessageForm(request.POST)
    if message_form.is_valid():
        data = message_form.cleaned_data
        content = data['message_content']
        time_sent = datetime.datetime.now()
        Message.objects.create_message(content, time_sent,recipient,sender)
    return render(request, 'messaging/direct_message.html',{'past_messages':messages, "form":message_form})
