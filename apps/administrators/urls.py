"""Circles URLs."""

# Django
from django.urls import path
from .views.administrators import *
# Views

from .views import *

urlpatterns = [
	path('home',AdminHomeView.as_view(),name="admin_home"),
	path('link-generator',LinkGeneratorView.as_view(),name="link_generator"),
	path('link-generator-final-step/<pk>',LinkGeneratorFinalStepView.as_view(),name="link_generator_final_step"),
	path('detail/<pk>',LinkDetailView.as_view(),name="detail"),
	path('opened-links',OpenedLinksView.as_view(),name="opened_links"),
	path('link/<pk>',LinksDeleteView.as_view(),name="delete_link"),
	path('cancel/<pk>',CancelView.as_view(),name="cancel_link"),

	path('link/get-link/<pk>',GetLinkView.as_view(),name="get_link"),
	path('link/final-link/<pk>',FinalLinkView.as_view(),name="final_link"),
	
	
	path('link/status-change/<pk>/<status>',StatusChangeView.as_view(),name="status_change"),
	path('link/set-date/<pk>',SetDateView.as_view(),name="set_date_view"),
	path('link/set-hour/<pk>',SetHourView.as_view(),name="set_hour_view"),

	path('configuration/',ConfigurationView.as_view(),name="configuration_view"),
]