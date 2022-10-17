from django import forms
from .models import User


class CreateAccount(forms.ModelForm):

	class Meta:
		USER_TYPES = ['Adopting a Pet', "Rehoming a Pet"]
		model = User
		fields = ['user_email', 'password', 'user_name', 'user_dob', 'user_address']
		profile_type = forms.RadioSelect(choices=USER_TYPES)

class Login(forms.ModelForm):


	class Meta:
		fields = ['user_email','password']
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