from django.db import models
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import get_user_model, authenticate, login

##

from students.utils import unique_slug_generator

User = settings.AUTH_USER_MODEL

class CountInfo(models.Model):
	creater		=	models.CharField(max_length = 100, null =True, blank = True)
	name 		=	models.CharField(max_length = 100, null =True, blank = True)	
	result 		=	models.IntegerField(null = True, blank = True)
	slug		=	models.SlugField(null = True, blank  = True)

	def get_absolute_url(self):
		return f'/counter/{self.slug}'

	@property
	def title(self):
		return self.name

	def __str__(self):
		return f'{self.name}--{self.creater}'

class CountUpdateInfo(models.Model):
	counter_r				=	models.ForeignKey(CountInfo, on_delete = 'CASCADE')
	action				=	models.CharField(max_length = 10, null = True, blank = True)
	action_count		=	models.IntegerField(null = True, blank = True)
	date_time 			=	models.DateTimeField(auto_now = True, null = True, blank = True)
	previous_value 		= 	models.IntegerField(null = True, blank = True)
	next_value 			= 	models.IntegerField(null = True, blank = True)
	operation_success	=	models.BooleanField(null = True, blank = True)

	def __str__(self):
		return f'{self.counter_r}---{self.action_count}---{self.date_time}'

	

def count_create(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)
	if not instance.result:
		instance.result = 0

def count_info_create(sender, instance, *args, **kwargs):
	try:
		obj 					= CountUpdateInfo.objects.filter(counter_r = instance.counter_r).latest('date_time')
		last_update 			= obj.action_count
		instance.action_count	= last_update + 1
	except:
		last_update				= 0
		instance.action_count	= 1
	try:
		previous_value		= obj.next_value
	except:
		previous_value		= 0
	instance.previous_value = previous_value
	if instance.action == 'up': instance.next_value = instance.previous_value + 1
	if instance.action == 'down': instance.next_value = instance.previous_value - 1
	instance.operation_success = True


pre_save.connect(count_create, sender = CountInfo)
pre_save.connect(count_info_create, sender = CountUpdateInfo)







