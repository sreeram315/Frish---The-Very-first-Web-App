from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, View
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from urllib.request import urlopen

# Create your views here.

from .forms import CountUrlForm
from .models import UrlInfo


class CreateForm(CreateView):
	form_class 		= 	CountUrlForm
	template_name 	= 	'shortenurl/create.html'						

class RedirectUrl(View):
	def get(self, request, *args, **kwargs):
		rlink = (UrlInfo.objects.filter(redirection_link = kwargs['rlink']).first()).original_link
		print(rlink)
		if rlink.startswith('http'):
			return HttpResponseRedirect(rlink)
		return HttpResponseRedirect('http://' + rlink)

class SucessView(TemplateView):
	template_name = 'shortenurl/success.html'

	def get_context_data(self, *args, **kwargs):
		context  = super(SucessView, self).get_context_data(*args, **kwargs)
		context['original_link']	=	UrlInfo.objects.get(redirection_link = kwargs['link']).original_link
		context['redirection_link']	=	UrlInfo.objects.get(redirection_link = kwargs['link']).redirection_link
		return context