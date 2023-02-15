"""DJANGO IMPORTS"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm


"""LOCAL MODELS"""
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
	add_form = CustomUserCreationForm
	form = CustomUserChangeForm
	model = CustomUser
	list_display = (
		'email', 
		'is_teacher',
		'is_owner',
		'is_director',
		'is_parent',
		'is_school_staff',
		'is_student',
		'is_superuser'
	)
	
	list_filter = ('email', 'is_staff', 'is_active',)

	fieldsets = (
		(None, {'fields': ('email', 'password','first_name','last_name')}),
		
		('Permissions', {'fields': (
			'is_teacher',
			'is_owner',
			'is_director',
			'is_parent',
			'is_school_staff',
			'is_student',
			'is_superuser'
		)}),
	)

	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': (
				'email',  
				'password1', 
				'password2',
				'is_teacher',
				'is_owner',
				'is_director',
				'is_parent',
				'is_school_staff',
				'is_student',
				'is_superuser'
			),
		}),
	)

	search_fields = ('email',)
	ordering = ('email',)
	filter_horizontal = ()

admin.site.register(CustomUser, CustomUserAdmin)
