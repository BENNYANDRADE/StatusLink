"""Profile model."""

# Django
from operator import truediv
from django.db import models
from django.conf import settings
from apps.utils.directory_path import user_profile_pic_directory_path
from django.contrib import admin

#Models
from apps.regions.models import Countries

class Profile(models.Model):
	""" Profile model.
		A profile holds a user's public data like biography, picture,
		and statistics.
	"""
	id_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	address = models.TextField(db_column='Address', blank=True, null=True)
	biography = models.TextField(db_column='Biography', blank=True, null=True)
	phone = models.CharField(db_column='Phone', max_length=15, blank=True, null=True)
	photo = models.ImageField('profile picture',db_column='Photo', upload_to = user_profile_pic_directory_path, blank=True, null=True)
	birthdate = models.DateField(db_column='BirthDate', blank=True, null=True)
	id_country = models.ForeignKey(Countries, models.DO_NOTHING, db_column='IdCountry',blank=True,null=True)
	is_public = models.BooleanField(db_column='IsPublic', default=True)
	
	def __str__(self):
		"""Return user's str representation."""
		return str(self.id_user)


admin.site.register(Profile)
