from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from .views import CountResultView, CountCreateUrl, CountUp, CountDown



urlpatterns = [
	url(r'^$', CountCreateUrl.as_view(), name = 'counter-create'),
	url(r'^(?P<slug>[\w-]*)$', CountResultView.as_view(), name = 'counter-view'),
	url(r'^(?P<slug>[\w-]*)/up$', CountUp.as_view(), name = 'counter-up'),
	url(r'^(?P<slug>[\w-]*)/down$', CountDown.as_view(), name = 'counter-down'),
	url(r'^$', CountCreateUrl.as_view(), name = 'counter-create'),
]

