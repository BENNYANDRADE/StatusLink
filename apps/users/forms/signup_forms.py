# Django
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import EmailInput, PasswordInput, TextInput,Select
from django import forms


class SignupMultipleUsersForm(UserCreationForm):
	
	USER_CHOICES = [
	   ('is_director','Director'),
	   ('is_teacher', 'Maestro'),
	   ('is_parent', 'Padre'),
	]
	
	options = forms.ChoiceField(choices = USER_CHOICES)

	class Meta:
		fields = ('email', 'first_name', 'last_name' ,'password1','password2','options')
		model = get_user_model()
		widgets = {
			'email': EmailInput(attrs={'placeholder': 'Correo electrónico'}),
			'first_name': TextInput(attrs={'placeholder': 'Nombre'}),
			'last_name': TextInput(attrs={'placeholder': 'Apellido'}),
			'password1': PasswordInput(attrs={'placeholder': 'Password'}),
			'password2': PasswordInput(attrs={'placeholder': 'Confirmación'}),
			'options': Select(attrs={'placeholder': 'Seleccione opcion'}),
		}
		

	def __init__(self, *args, **kwargs):
		super(SignupMultipleUsersForm, self).__init__(*args, **kwargs)

		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'
			# visible.field.help_text = None
				
	def clean_username(self):
		User = get_user_model()
		username=self.cleaned_data.get('email')

		if User.objects.filter(username=username).exists():
			raise forms.ValidationError('¡El usuario ya existe!')

		return username
	
	def clean_options(self):
		options = self.cleaned_data.get('options')
		if options == "is_director" or options == "is_teacher" or options == "is_parent":
			return options
		else:
			raise forms.ValidationError('¡No se selecciono opción!')
