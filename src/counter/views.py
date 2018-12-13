from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, View
from django.db.models import Q, F



# code here

from .models import CountInfo, CountUpdateInfo
from .forms import CounterCreateForm

class CountCreateUrl(CreateView):
	form_class = CounterCreateForm
	template_name = 'counter/create.html'


class CountResultView(DetailView):
	template_name	=	'counter/result_view.html'

	def get_queryset(self, *args, **kwargs):
		slug = self.kwargs.get('slug')
		queryset = CountInfo.objects.filter(slug = slug)
		return queryset

	def get_context_data(self, *args, **kwargs):
		context 	= super(CountResultView, self).get_context_data(*args, **kwargs)
		counter_r	= CountInfo.objects.get(slug = self.kwargs.get('slug'))
		details		= CountUpdateInfo.objects.filter(counter_r = counter_r).order_by('date_time').reverse()
		context['details']	=	details
		return context

class CountUp(View):
	def get(self, request,  *args, **kwargs):
		slug = self.kwargs['slug']
		obj = CountInfo.objects.get(slug=slug)
		CountInfo.objects.filter(slug=slug).update(result= F('result') + 1)
		CountUpdateInfo.objects.create( counter_r = obj, 
										action = 'up'
										)
		return redirect(f'/counter/{slug}')

class CountDown(View):
	def get(self, request,  *args, **kwargs):
		slug = self.kwargs['slug']
		obj = CountInfo.objects.get(slug=slug)
		CountInfo.objects.filter(slug=slug).update(result= F('result') - 1)
		CountUpdateInfo.objects.create( counter_r = obj, 
										action = 'down',
										)
		return redirect(f'/counter/{slug}')








