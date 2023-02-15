""" User's Views """

# Django
from datetime import datetime
from django.contrib.auth.views import LoginView
from django.views.generic import View,CreateView,TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages 
from django.conf import settings
from django.contrib.auth import authenticate,logout,login,get_user_model
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.core.mail import EmailMessage
from django.db import transaction,IntegrityError


# local Django
from apps.utils.tokens import account_activation_token
from ..forms import SignupMultipleUsersForm

User = get_user_model()

class LoginView(LoginView):
	template_name = 'users/login.html'
	def post(self,request):
		# username = request.POST['email']
		# password = request.POST['password']
		# user = authenticate(email=username, password=password)
		# print('verificar',user)
		# if user is None:
		# 	messages.add_message(request, messages.INFO, '¡Credenciales inválidas!', extra_tags="danger")
		# if user is not None:
		# 	if user.is_active:
		# 		if user.last_login is None:
		# 			login(request, user)
		return HttpResponseRedirect(reverse('administrators:admin_home'))
		# 		else:
		# 			login(request, user)
					
		# 			return HttpResponseRedirect(reverse('users:'))
		# 	else:
		# 		print('usuario inactivo')
		# 		return HttpResponse("Inactive user.")
		# else:
		# 	return HttpResponseRedirect(settings.LOGIN_URL)
		
			
class LogoutView(View):
	def get(self, request):
		logout(request)
		return HttpResponseRedirect(settings.LOGIN_URL)


class ActivateAccount(View):
	def get(self, request, uidb64, token, *args, **kwargs):
		try:
			uid = force_str(urlsafe_base64_decode(uidb64))
			user = User.objects.get(pk=uid)
		except (TypeError, ValueError, OverflowError, User.DoesNotExist):
			user = None

		if user is not None and account_activation_token.check_token(user, token):
			user.is_active = True
			user.email_confirmed = True
			user.save()
			login(request, user)
			messages.add_message(self.request, messages.SUCCESS, f"¡Su cuenta ha sido activada!",extra_tags='success')

			# messages.success(request, ('Your account have been confirmed.'))

			if user.is_teacher:
				return HttpResponseRedirect(reverse('users:login'))
			elif user.is_owner:
				return HttpResponseRedirect(reverse('users:login'))
			elif user.is_parent:
				return HttpResponseRedirect(reverse('users:login'))
			elif user.is_director:
				return HttpResponseRedirect(reverse('users:login'))
			elif user.is_student:
				return HttpResponseRedirect(reverse('users:login'))
		else:
			messages.warning(request, ('El link de confirmación es inválido'))
			return HttpResponseRedirect(reverse('users:login'))


class EmailConfirmView(TemplateView):
	def get(self, request, **kwargs):     
		return render(request, 'users/email_confirm.html')


class PasswordChangeView(View):
	template_name = 'users/password_change.html'
	
	def get(self, request, **kwargs):
		return render(request, 'users/password_change.html')

	def post(self, request, **kwargs):   
		user = self.request.user
		user.last_login = datetime.today()
		user.set_password(self.request.POST['password'])
		user.save()
		messages.add_message(self.request, messages.SUCCESS, f"¡Contraseña actualizada!",extra_tags='success')

		if user.is_teacher:
			return HttpResponseRedirect(reverse('users:login'))
		elif user.is_student:
			return HttpResponseRedirect(reverse('users:login'))
		elif user.is_parent:
			return HttpResponseRedirect(reverse('users:login'))
		elif user.is_director:
			return HttpResponseRedirect(reverse('users:login'))
		elif user.is_owner:
			return HttpResponseRedirect(reverse('users:login'))


class SignupMultipleUsersView(CreateView):
	form_class = SignupMultipleUsersForm
	success_url = reverse_lazy("users:login")
	template_name = "users/signup_multiple_options.html"

	def post(self, request):
		form = self.form_class(request.POST)

		if form.is_valid():
			options = form.cleaned_data['options']

			try: 
				with transaction.atomic(): 
					user = form.save(commit=False)
					user.username = user.email
					user.set_password(self.request.POST['password1'])
					if options == "is_teacher":
						user.is_teacher = True
					elif options == "is_parent":
						user.is_parent = "True"
					elif options == "is_director":
						user.is_director = True
					user.save()

					try:
						"""Send account verification link"""
						current_site = get_current_site(request)
						subject = 'Hi {} , please verify your account'.format(user.email)
						from_email = 'GoHives <noreply@gohives.com>'
						# text_content = 'GoHives <noreply@gohives.com>'
						message = render_to_string('users/account_activation_email.html', {
							'user': user,
							'domain': current_site.domain,
							'uid': urlsafe_base64_encode(force_bytes(user.pk)),
							'token': account_activation_token.make_token(user),
						})
						msg = EmailMessage(subject, message, from_email, [user.email])
						msg.content_subtype = 'html'
						msg.send()
					except Exception as e:
						print('error al enviar mail, linea 117',e)
			except IntegrityError as e: 
				print('Error al crear usuario',e)

			return HttpResponseRedirect(reverse('users:email_confirm'))
		
		return render(request, self.template_name, {'form': form})
