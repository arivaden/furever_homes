from django.test import TestCase
import models
# Create your tests here.

#DATABASE STUFF TEST CODE
class UserTestCases(TestCase):
	def make_User(self):
		models.User.objects.create_user('test@gmail.com', 'password', user_name="Jon Doe")
		models.CurrentOwner.objects.create_user('co@gmail.com', 'secret_password', user_name='Ms. Current Owner')
		models.FutureOwner.objects.create_user('fo@gmail.com', 'secret_password123', user_name='Mr. Future Owner')
		models.Moderator.objects.create_staffuser('mod@fureverhomes.com', 'mod_password', user_name = 'mrs. mod')

	def test_getName(self):
		jon = models.User.objects.get_by_natural_key('test@gmail.com')
		co = models.CurrentOwner.objects.get_by_natural_key('co@gmail.com')
		fo = models.FutureOwner.objects.get_by_natural_key('fo@gmail.com')
		mod = models.Moderator.objects.get_by_natural_key('mod@fureverhomes.com')
		self.assertEqual(jon.getName(), 'Jon Doe')
		self.assertEqual(co.getName(), 'Ms. Current Owner')
		self.assertEqual(fo.getName(), 'Mr. Future Owner')
		self.assertEqual(mod.getName(), 'mrs. mod')

