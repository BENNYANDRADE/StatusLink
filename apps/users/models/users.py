"""User's models."""


# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from ..managers import CustomUserManager


class CustomUser(AbstractUser,):
	"""User model.
	Extend from Django's Abstract User, change the username field
	to email and add some extra fields.
	"""
	username = None
	first_name = models.CharField("first name", max_length=150, blank=True)
	last_name = models.CharField("last name", max_length=150, blank=True)
	
	email = models.EmailField(
		'email address',
		unique=True,
		error_messages={
			'unique': 'A user with that email already exists.'
		}
	)   
	email_confirmed = models.BooleanField(
		'verified',
		default=False,
		help_text='Set to true when the user have verified its email address.'
	)

	is_teacher = models.BooleanField(db_column='IsTeacher',default=False)
	is_owner = models.BooleanField(db_column='IsOwner',default=False)
	is_director = models.BooleanField(db_column='IsDirector',default=False)
	is_parent = models.BooleanField(db_column='IsParent',default=False)
	is_school_staff = models.BooleanField(db_column='IsSchoolStaff',default=False)
	is_student = models.BooleanField(db_column='IsStudent',default=False)
	creation_date = models.DateField(db_column='CreationDate',blank=True, null=True)
	
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name','last_name']
	
	objects = CustomUserManager()
	
	def __str__(self):
		"""Return username."""
		return self.email

