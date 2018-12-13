from django.conf.urls import url
from django.contrib import admin
from .views import TwitterHomeView, TwitterCreateView
from django.views.generic import TemplateView



urlpatterns = [
    url(r'^$', TwitterHomeView.as_view(), name = 'twitter-home'),
    url(r'^new-tweet/$', TwitterCreateView.as_view(), name = 'twitter-newtweet'),
]
