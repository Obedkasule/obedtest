

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

#====================user information to be collected==========================
class UserInfo(AbstractUser):

	date_joined = models.DateTimeField(auto_now_add = True)
	uid = models.CharField(max_length = 10, primary_key = True)
	username = models.CharField(max_length = 10, null = True)
	first_name = models.CharField(max_length = 15)
	last_name = models.CharField(max_length = 35)
	email = models.EmailField(max_length = 50, unique=True)
	telephoneNumber = models.CharField(max_length = 15)
	is_active = models.BooleanField(default = True)
	is_staff = models.BooleanField(default = True)
	password = models.CharField(max_length = 10)
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['telephoneNumber']

	

	def get_full_name():
		return firstName +" "+ otherNames