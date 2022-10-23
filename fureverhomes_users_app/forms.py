from django import forms
from .models import User, CurrentOwner, FutureOwner
from django.contrib.auth.forms import UserCreationForm


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


class CreateFOAccount(forms.ModelForm):

	class Meta:
		model = FutureOwner
		fields = ['user_email', 'password', 'user_name', 'user_dob', 'user_zip']


class GetPreferences(forms.ModelForm):

	class Meta:
		model = FutureOwner
		fields = ['type_pref', 'size_pref', 'age_pref', 'sex_pref', 'kids_pref', 'fixed_pref']

class Login(forms.ModelForm):

	class Meta:
		fields = ['user_email', 'password']
		model = User
		'''
#first name
forms.CharField()
#last name
forms.CharField()
#email
forms.EmailField()
#password (will have requirements, at least 8 characters, num/char mix)
forms.RegexField() '''