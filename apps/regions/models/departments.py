"""Departments's models."""

# Django
from django.db import models
from django.contrib import admin

class Departments(models.Model):
    id = models.AutoField(db_column='IdDepartment', primary_key=True)
    name = models.CharField(db_column='Name', max_length=20)

    class Meta:
        
        db_table = 'Departments'
    
    def __str__(self):
        """Return event department name."""
        return self.name

admin.site.register(Departments)
