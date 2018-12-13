from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.contrib.auth import get_user_model
from .forms import NewTweetForm
from accounts.models import AccountInfo
from .models import TweetInfo

User = get_user_model()


class TwitterHomeView(LoginRequiredMixin, TemplateView):
	template_name = 'twitter/home.html'

	def get_context_data(self, *args, **kwargs):
		following 	=	self.request.user.is_following.all()
		context = {'name': 'Sreeram Reddy Maram'}
		following = [i.owner for i in following]
		following += [self.request.user]		# following himself
		tweets = TweetInfo.objects.filter(owner__in = following).order_by('-date_time')
		
		for tweet in tweets:
			tweet.name 		= AccountInfo.objects.get(owner = tweet.owner).name
			tweet.username 	= AccountInfo.objects.get(owner = tweet.owner).username
			tweet.user_link	= AccountInfo.objects.get(owner = tweet.owner).slug
		context['tweets'] 	= tweets
		print(tweets)

		return context


class TwitterCreateView(LoginRequiredMixin ,CreateView):
	form_class 		=  NewTweetForm
	template_name 	= 'twitter/new-tweet.html'
	success_url 	= '/twitter/'
	login_url		= '/login/'

	def form_valid(self, form):
		instance 		= form.save(commit = False)
		instance.owner 	= self.request.user
		return super(TwitterCreateView, self).form_valid(form)

	def get_context_data(self, *args, **kwargs):
		context 			= super(TwitterCreateView, self).get_context_data(*args, **kwargs)
		context['title']	= 'New Tweet'
		print(context)
		return context
