from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from .views import CreateForm, SucessView



urlpatterns = [
	url(r'^$', CreateForm.as_view(), name = 'shortenurl-create'),
	url(r'^success/(?P<link>[\w-]*)/$', SucessView.as_view(), name = 'shortenurl-success'),
]

