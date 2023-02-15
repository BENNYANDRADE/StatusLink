"""Municipalities's models."""

# Django
from django.db import models
from django.contrib import admin

class Municipalities(models.Model):
    id = models.AutoField(db_column='IdMunicipality', primary_key=True)
    name = models.CharField(db_column='Name', max_length=150)

    class Meta:
        db_table = 'Municipalities'
    
    def __str__(self):
        """Return event municipalities name."""
        return self.name

admin.site.register(Municipalities)
