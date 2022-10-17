from django import forms
import models


class CreateAccount(forms.ModelForm):

	class Meta:
		USER_TYPES = ['Adopting a Pet', "Rehoming a Pet"]
		model = models.User
		fields = ['email', 'password', 'name', 'dob', 'address']
		profile_type = forms.RadioSelect(choices=USER_TYPES)

		'''
#first name
forms.CharField()
#last name
forms.CharField()
#email
forms.EmailField()
#password (will have requirements, at least 8 characters, num/char mix)
forms.RegexField() '''