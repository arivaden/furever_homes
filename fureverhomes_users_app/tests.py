from django.test import TestCase
from .models import User, CurrentOwner, FutureOwner, Moderator, PetProfile, Dog, Cat, Message
# Create your tests here.

#DATABASE STUFF TEST CODE
class UserTestCases(TestCase):
	def make_User(self):
		j = User.objects.create_user('test@gmail.com', 'password', user_name="Jon Doe")
		c = CurrentOwner.objects.create_user('co@gmail.com', 'secret_password', user_name='Ms. Current Owner')
		f = FutureOwner.objects.create_user('fo@gmail.com', 'secret_password123', user_name='Mr. Future Owner')
		m = Moderator.objects.create_staffuser('mod@fureverhomes.com', 'mod_password', user_name = 'mrs. mod')

	def make_Pet(self):
		pet1 = Dog(pet_name='Charlie', description='a friendly dog')

	'''def test_getName(self):
		co = CurrentOwner.objects
		fo = FutureOwner.objects.get_by_natural_key('fo@gmail.com')
		mod = Moderator.objects.get_by_natural_key('mod@fureverhomes.com')
		self.assertEqual(jon.getName(), 'Jon Doe')
		self.assertEqual(co.getName(), 'Ms. Current Owner')
		self.assertEqual(fo.getName(), 'Mr. Future Owner')
		self.assertEqual(mod.getName(), 'mrs. mod') '''

