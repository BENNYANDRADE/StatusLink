"""Departments's models."""

# Django
from django.db import models
from django.contrib import admin
from  apps.utils.directory_path import file_path


class LinkInfo(models.Model):
	id = models.AutoField(db_column='IdDepartment', primary_key=True)
	link_name = models.CharField(db_column='Name', max_length=150,blank=True, null=True)
	generated_link = models.CharField(db_column='GeneratedLink', max_length=20,blank=True, null=True)
	comments = models.TextField(db_column='Comment',blank=True, null=True)
	attachment = models.FileField(db_column='Attachment', upload_to = file_path, blank=True, null=True)

	class Meta:
		
		db_table = 'LinkInfo'
	
	def __str__(self):
		"""Return event department name."""
		return self.link_name


class ProcessStatus(models.Model):
	id = models.AutoField(db_column='IdProcessStatus', primary_key=True)
	description = models.CharField(db_column='Description', max_length=150,blank=True, null=True)
	
	class Meta:
		
		db_table = 'ProcessStatus'
	
	def __str__(self):
		"""Return event department name."""
		return self.description


class ProcessSteps(models.Model):
	id = models.AutoField(db_column='IdProcessExtra', primary_key=True)
	step_name = models.TextField(db_column='StepName')
	link_info = models.ForeignKey(LinkInfo, on_delete=models.CASCADE, db_column='IdLinkInfo')
	process_status = models.ForeignKey(ProcessStatus, on_delete=models.CASCADE, db_column='ProcessStatus')
	# process_status = models.ForeignKey(ProcessStatus, on_delete=models.CASCADE, db_column='ProcessStatus')
	register_date = models.DateField(db_column='RegisterDate', auto_now_add=True, blank=True)
	calendar_date = models.DateField(db_column='CalendarDate', blank=True,null=True)
	# register_time= models.TimeField(db_column='RegisterTime', blank=True)
	# calendar_time= models.TimeField(db_column='CalendarTime', blank=True)
	register_date_time  = models.DateTimeField(db_column="RegisterDateTime",blank=True,null=True)
	progress = models.IntegerField(default=0,blank=True,null=True)
	hours = models.IntegerField(default=0,blank=True,null=True)
	class Meta:
		
		db_table = 'ProcessSteps'
	
	def __str__(self):
		"""Return event department name."""
		return self.step_name


admin.site.register(LinkInfo)
admin.site.register(ProcessSteps)
admin.site.register(ProcessStatus)
