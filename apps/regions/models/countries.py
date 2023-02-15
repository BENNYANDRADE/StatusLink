"""Countries's models."""

# Django
from django.db import models
from django.contrib import admin


#Locals
class Countries(models.Model):
	id = models.AutoField(db_column='IdCountry', primary_key=True)
	name = models.CharField(db_column='CountryName', max_length=350)

	class Meta:
		
		db_table = 'Countries'
	
	def __str__(self):
		"""Return event country name."""
		return self.country_name

admin.site.register(Countries)

