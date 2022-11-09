import django
import os
from django.db import models
#from django.conf import settings
#settings.configure()
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core import validators


class UserManager(BaseUserManager):
	use_in_migrations = True

	def save_user(self, email, password, user_dob, user_zip, **extra_fields):
		#Creates and saves a User with the given email and password.
		if not email:
			raise ValueError('The given email must be set')
		if not password:
			raise ValueError('You must create a password')

		email = self.normalize_email(email)
		user = self.model(
			user_email=email,
			**extra_fields)

		# Call this method for password hashing
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password=None, user_dob=None, user_zip=None, **extra_fields):
		extra_fields['is_superuser'] = False
		extra_fields['is_staff'] = False
		return self.save_user(email, password, user_dob, user_zip, **extra_fields)

	# Method called while creating a staff user
	def create_staffuser(self, email, password, **extra_fields):
		extra_fields['is_staff'] = True
		extra_fields['is_superuser'] = False

		return self.save_user(email, password, **extra_fields)

	# Method called while calling creatsuperuser
	def create_superuser(self, email, password, **extra_fields):

		# Set is_superuser parameter to true
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_superuser') is not True:
			raise ValueError('is_superuser should be True')

		extra_fields['is_staff'] = True

		return self.save_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
	user_id = models.BigAutoField(primary_key=True)
	user_email = models.CharField(default="youremail@example.com", unique=True, blank=False, max_length=30, validators=[validators.EmailValidator()])
	user_name = models.CharField(max_length=50, blank=False, default="YourName")
	user_dob = models.DateField(blank=False, default='1999-01-01')
	user_zip = models.CharField( default=10000, blank=False, max_length=5, validators=[validators.RegexValidator(r'^\d{1,10}$')])
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)  # used for blocking, will be set false by moderator
	USERNAME_FIELD = 'user_email'
	objects = UserManager()

	def getName(self):
		return self.user_name


#these are subclasses of User
class FutureOwner(User):
	fo_id = User.user_id
	pet_type = [('dog', 'Dog'), ('cat', 'Cat')]
	pet_sex = [('M', "Male"), ('F', 'Female'), ('N',"No Preference")]
	pet_age = [(0, 'Young'), (1, "Adult"), (2, "Senior")]
	good_w_kids = [(0, 'Must be good with kids'), (1, "Doesn't need to be good with kids")]
	spayed_or_neutered = [(0, 'Must be spayed/neutered'), (1, "Doesn't need to be spayed/neutered")]
	size = [(1, "Small"), (2, "Medium"), (3, "Large"), (4, "No Preference")]
	size_pref = models.IntegerField(default=4, choices=size)
	type_pref = models.TextField(default='dog', max_length=5, choices=pet_type)
	sex_pref = models.CharField(default='N', max_length=3, choices=pet_sex)
	age_pref = models.IntegerField(default=0, choices=pet_age)
	kids_pref = models.IntegerField(default=0, choices=good_w_kids)
	fixed_pref = models.IntegerField(default=0, choices=spayed_or_neutered)

	# user can input preferences specific for dogs/cats
	def specific_preferences(self):
		pass

	# returns QuerySet of pet profiles based on User's preferences
	def find_pets(self):
		#Determine pet type
		if self.type_pref == 'dog':
			pet_pool = Dog.objects.filter(age=self.age_pref).exclude(is_adopted=True)
		else:
			pet_pool = Cat.objects.filter(age=self.age_pref).exclude(is_adopted=True)

		#filter with extra criteria
		if self.sex_pref == 'M' or self.sex_pref == 'F':
			pet_pool = pet_pool.filter(sex=self.sex_pref)
		if self.kids_pref == 0:
			pet_pool = pet_pool.filter(good_w_kids=True)
		if self.fixed_pref == 0:
			pet_pool = pet_pool.filter(spayed_or_neutered=True)
		if self.size_pref != 4:
			pet_pool = pet_pool.filter(size = self.size_pref)

		return pet_pool

	# allows user to change preferences, must specify name of field being updated
	def edit_preferences(self, type_pref=None, size_pref=None, age_pref=None, sex_pref=None, kids_pref=None, fixed_pref=None):
		if type_pref is not None:
			self.type_pref = type_pref
		if size_pref is not None:
			self.size_pref = size_pref
		if age_pref is not None:
			self.age_pref = age_pref
		if sex_pref is not None:
			self.sex_pref = sex_pref
		if kids_pref is not None:
			self.kids_pref = kids_pref
		if fixed_pref is not None:
			self.fixed_pref = fixed_pref
		self.save()

	def to_CO(self):
		new_co = CurrentOwner.objects.create_user(email=self.user_email, password=self.password, user_dob=self.user_dob, user_zip=self.user_zip)
		new_co.user_id = self.user_id
		new_co.user_name = self.user_name
		new_co.save()
		self.delete()

class CurrentOwner(User):
	co_id = User.user_id

	def view_my_pets(self):
		co_pets = PetProfile.objects.filter(current_owner=self.user_id).exclude(is_adopted=True)
		return co_pets

	def view_my_adopted_pets(self):
		co_pets = PetProfile.objects.filter(current_owner=self.user_id, is_adopted=True)
		return co_pets

	def to_FO(self):
		if len(self.view_my_pets()) == 0:
			new_fo = FutureOwner.objects.create_user(email=self.user_email, password=self.password, user_dob=self.user_dob, user_zip=self.user_zip)
			new_fo.user_id = self.user_id
			new_fo.user_name = self.user_name
			new_fo.save()
			self.delete()
		else:
			raise Exception("Cannot adopt a pet while you still have pets up for adoption.")

#moderator can block other users
class Moderator(User):
	mod_id = User.user_id

	def block_user(self, user_to_block):
		user_to_block.is_active = False


class Report(models.Model):
	report_id = models.AutoField(primary_key=True)
	report_made_dt = models.DateTimeField
	incident_dt = models.DateField
	causes = ((1, 'Threatening Language'), (2, 'Demand of Payment'), (3, 'Surrender of puppies under 8/kittens under 10 weeks'), (4, 'Other')) #complete later
	report_cause = models.IntegerField(choices=causes)
	report_images = models.ImageField(blank=True, upload_to='report_photos')
	user_reported = models.ForeignKey(User, models.CASCADE, related_name='reported')
	user_reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reporter')
	moderator_assigned = models.ForeignKey(Moderator, on_delete=models.PROTECT)


class Message(models.Model):
	message_id = models.BigAutoField(primary_key = True)
	message_dt = models.DateTimeField
	message_content = models.CharField(max_length=1000)
	receiver_id = models.ForeignKey(User, models.CASCADE, related_name='receiver')
	sender_id = models.ForeignKey(User, models.CASCADE, related_name='sender')


class PetManager(models.Manager):

	def create_pet_profile(self, co, pet_name, **extra_fields):
		extra_fields['is_adopted'] = False
		#date will automatically be added, like id
		if not pet_name:
			raise ValueError('You must give the name of your pet')
		pet = self.model(pet_name=pet_name, current_owner=co, **extra_fields)
		pet.save(using=self._db)
		return pet



class PetProfile(models.Model):
	pet_profile_id = models.AutoField(primary_key=True)
	pet_name = models.CharField(max_length=30)
	description = models.CharField(max_length=300)
	profile_pic = models.ImageField(blank=True, upload_to='pet_profile_photos')
	age_choices = [(0, 'Young: 0-1 Years'), (1, "Adult: 1-6 Years"), (2, "Senior: 6+ Years")]
	age = models.IntegerField(choices=age_choices, default=0)
	sexes = (('M', 'Male'), ('F', 'Female'), ('U', 'Unsure'))
	sex = models.CharField(max_length=1, choices=sexes, default='U')
	size_choices = ((1, "Small"), (2, "Medium"), (3, "Large"))
	size = models.IntegerField(choices=size_choices, default=2)
	good_w_kids = models.BooleanField(default=False)
	spayed_or_neutered = models.BooleanField(default=False)
	rehoming_reason = models.CharField(max_length=200)
	date_uploaded = models.DateField(auto_now_add=True)
	is_adopted = models.BooleanField(default=False)
	current_owner = models.ForeignKey(to=CurrentOwner, on_delete=models.CASCADE)
	interested_users = models.ManyToManyField(FutureOwner)
	objects = PetManager()

	class Meta:
		ordering = ["date_uploaded"]


class Dog(PetProfile):
	breed = models.CharField(max_length=20)


class Cat(PetProfile):
	is_declawed = models.BooleanField(default=False)
