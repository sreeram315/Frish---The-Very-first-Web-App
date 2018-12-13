from django.db import models
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.contrib.auth import get_user_model, authenticate, login


# Create your models here.

from .utils import unique_slug_generator, random_string_generator

User = settings.AUTH_USER_MODEL

class AccountInfoManager(models.Manager):
	def toggle_follow(self, user_follower, user_following):
		if user_follower not in user_following.followers.all():
			user_following.followers.add(user_follower)
		else:
			user_following.followers.remove(user_follower)

class AccountInfo(models.Model):
	owner		=	models.OneToOneField(User, on_delete = models.CASCADE)
	name		=	models.CharField(max_length = 100, null = True, blank = True)
	username	=	models.CharField(max_length = 100, null = True, blank = True)
	email		=	models.CharField(max_length = 100, null = True, blank = True)
	dob			=	models.DateField(null = True, blank  = True)
	contact		=	models.IntegerField(null = True, blank  = True)
	address		=	models.CharField(max_length = 300, null = True, blank = True)
	updated		=	models.DateTimeField(auto_now = True, null = True, blank = True)
	activation_key	=	models.CharField(max_length = 50, null = True, blank = True)
	activated	=	models.BooleanField(default = False)
	followers	=	models.ManyToManyField(User, blank = True, related_name = 'is_following')
	slug		=	models.SlugField(null = True, blank  = True)
	description	=	models.CharField(max_length = 9999, blank = True, null = True)


	objects = AccountInfoManager()

	def __str__(self):
		return f'{self.name} ({self.username})'

	def send_activation_email(self):
		print('SENDING EMAIL')
		if not self.activated:
			self.activation_key	=	random_string_generator(size = 35)
			self.save()
			subject = 'Activate your sreeram.rocks account'
			from_email = settings.DEFAULT_FROM_EMAIL
			message = f'Activate you account here: {self.activation_key}'
			recipient_list	=	[self.email]
			html_message = f'<p> Acitvate your account: {self.activation_key}</p>'
			sent_mail = send_mail(
				subject, message, from_email, 
				recipient_list, fail_silently = False,
				 html_message = html_message
				)
			return sent_mail

	def login_re(self, username, password):
		print('logging in')




	@property
	def title(self):
		return self.name
	
# def pre_info_post_save(sender, instance, *args, **kwargs):
# 	if not instance.name:
# 		instance.name = instance.username.capitalize()

def prof_info_post_save(sender, instance, created, *args, **kwargs):
	print(kwargs)
	if created:
		profile, is_created = AccountInfo.objects.get_or_create(owner = instance, name = instance.username, email = instance.email,  username = instance.username)

def prof_clug_pre_save(sender, instance, *args, **kwargs):
	print('saving')
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)

# pre_save.connect(pre_info_post_save, sender = User)
post_save.connect(prof_info_post_save, sender = User)

pre_save.connect(prof_clug_pre_save, sender = AccountInfo)




