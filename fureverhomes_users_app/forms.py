from django import forms
from .models import User, CurrentOwner, FutureOwner
from django.contrib.auth.forms import UserCreationForm


class CreateAccount(forms.ModelForm):

	class Meta:
		USER_TYPES = ['Adopting a Pet', "Rehoming a Pet"]
		model = User
		fields = ['user_email', 'password', 'user_name', 'user_dob', 'user_zip']
		profile_type = forms.RadioSelect(choices=USER_TYPES)


class CreateCOAccount(forms.ModelForm):

	class Meta:
		model = CurrentOwner
		fields = ['user_email', 'password', 'user_name', 'user_dob', 'user_zip']


class CreateFOAccount(forms.ModelForm):

	class Meta:
		model = FutureOwner
		fields = ['user_email', 'password', 'user_name', 'user_dob', 'user_zip']


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