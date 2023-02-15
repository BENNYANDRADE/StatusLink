# Django
from django.contrib.auth.forms import UserCreationForm ,UserChangeForm

# LOCAL MODELS
from ..models import CustomUser


class CustomUserCreationForm(UserCreationForm):
	
	class Meta:
		model = CustomUser
		fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
	
	class Meta:
		model = CustomUser
		fields = ('email',)