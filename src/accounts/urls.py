from django.conf.urls import url
from django.contrib import admin
from .views import (
	AccountProfileView, AccountUpdateView, AccountOpenProfileView, 
	AccountFollowToggle, AccountListView, RegisterAccount
	)
from django.views.generic import TemplateView



urlpatterns = [
	url(r'^profile/$', AccountProfileView.as_view(), name = 'account-profile'),
	url(r'^register/$', RegisterAccount.as_view(), name = 'account-register'),
	url(r'^(?P<slug>[\w-]*)$', AccountOpenProfileView.as_view(), name = 'account-openprofile'),
	url(r'^(?P<slug>[\w-]*)/update$', AccountUpdateView.as_view(), name = 'account-update'),
	url(r'^follow/$', AccountFollowToggle.as_view(), name = 'account-follow'),
	url(r'^account-list/$', AccountListView.as_view(), name = 'account-list'),
]

