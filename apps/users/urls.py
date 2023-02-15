"""Circles URLs."""

# Django
from django.urls import path


# Views

from .views import *

urlpatterns = [
	path('',LoginView.as_view(),name="login"),
	path('users/logout',LogoutView.as_view(),name="logout"),

	#SIGNUP
	
	# path('users/parent-signup',ParentSignupView.as_view(),name="parent_signup"),
	path('users/signup-options',SignupMultipleUsersView.as_view(),name="signup_multiple_users"),
	path('users/password-change',PasswordChangeView.as_view(),name="password_change"),
	path('users/email_confirm',EmailConfirmView.as_view(),name="email_confirm"),
	path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
]