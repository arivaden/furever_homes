from django import forms
from .models import User, CurrentOwner, FutureOwner, PetProfile, Dog, Cat, Message
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm

# do not delete, want to try and get this to work with dynamically generating forms

class PetType(forms.Form):
	pets = [('d','Dog'), ('c',"Cat")]
	pet_type = forms.RadioSelect(choices=pets)

#parent form for pet forms
class PetForm(forms.ModelForm):
	class Meta:
		model = PetProfile
		fields = ['pet_name', 'description', 'profile_pic', 'age',
				  'sex', 'size', 'good_w_kids', 'spayed_or_neutered', 'rehoming_reason']
		labels = {
			'pet_name': _("Name"),
			'description': _("A short description of your pet so people can get to know them better"),
			'profile_pic':_("Profile Photo"),
			'age': _("Pet's age"),
			'sex': _("Gender"),
			'size': _("Size"),
			'good_w_kids': _("Is the pet comfortable with children?"),
			'spayed_or_neutered': _('Are they spayed/neutered?'),
			'rehoming_reason': _("Please give a little information about why you're rehoming your pet")

			}
		help_texts = {
			'age': _("""Note, we do not take puppies under 8 weeks or kittens under 10 weeks. 
						If you are attempting to give away animals under this age you are in violation of our community guidelines
						and will possibly be banned from the site or reported to the authorities."""),
			'good_w_kids': _("If you're unsure, please don't check the box."),
			'spayed_or_neutered': _("If you don't know if your pet is spayed/neutered, please don't check the box."),

			}

class DogForm(PetForm):
	class Meta(PetForm.Meta):
		model = Dog
		fields = ['pet_name', 'description', 'profile_pic', 'age',
				  'sex', 'size', 'good_w_kids', 'spayed_or_neutered', 'rehoming_reason', 'breed']
		labels = {'breed': _("Breed")}

class CatForm(PetForm):
	class Meta(PetForm.Meta):
		model = Cat
		fields = ['pet_name', 'description', 'profile_pic', 'age',
				  'sex', 'size', 'good_w_kids', 'spayed_or_neutered', 'rehoming_reason', 'is_declawed']
		labels = {'is_declawed': _("Is your cat declawed?")}

class getUserProfile(forms.Form):

	class Meta:
		USER_TYPES = [('fo', 'Adopting a Pet'), ('co', "Rehoming a Pet")]
		profile_type = forms.RadioSelect(choices=USER_TYPES)
		'''if profile_type == 'fo':
					model = FutureOwner
				else:
					model = CurrentOwner'''


class CreateAccount(forms.ModelForm):

	class Meta:

		fields = ['user_email', 'password', 'user_name', 'user_dob', 'user_zip']



class CreateCOAccount(forms.ModelForm):

	class Meta:
		model = CurrentOwner
		fields = ['user_email', 'password', 'user_name', 'user_dob', 'user_zip']
		labels = {
			'user_email': _('Email'),
			'password' : _("Password"),
			'user_dob' : _("Date of Birth"),
			'user_zip': _("Zipcode")

		}

		help_texts = {
			'user_dob': "YYYY-MM-DD format"
		}


class CreateFOAccount(forms.ModelForm):

	class Meta:
		model = FutureOwner
		fields = ['user_email', 'password', 'user_name', 'user_dob', 'user_zip']
		labels = {
			'user_email': _('Email'),
			'password': _("Password"),
			'user_dob': _("Your date of Birth"),
			'user_zip': _("Zipcode")

		}

		help_texts = {
			'user_dob' : "YYYY-MM-DD format"
		}

class GetPreferences(forms.ModelForm):

	class Meta:
		model = FutureOwner
		fields = ['type_pref', 'size_pref', 'age_pref', 'sex_pref', 'kids_pref', 'fixed_pref']
		labels = {
			'type_pref': _('What kind of pet are you looking for?'),
			'size_pref': _("Size"),
			'age_pref': _("Age"),
			'sex_pref': _("Gender"),
			'kids_pref': _("Should the pet be good with kids?"),
			'fixed_pref': _("Should the pet be fixed?")

		}

class Login(forms.ModelForm):

	class Meta:
		fields = ['user_email', 'password']
		model = User


class MessageForm(forms.ModelForm):
	class Meta:
		model = Message
		fields = ['message_content']
		help_texts = { 'message_content' : _("Write your message, but please keep it under 1000 characters") }
		error_messages = {"message_content" : {"max_length": _("Your message is too long. Please shorten it.") } }



		'''
#first name
forms.CharField()
#last name
forms.CharField()
#email
forms.EmailField()
#password (will have requirements, at least 8 characters, num/char mix)
forms.RegexField() '''