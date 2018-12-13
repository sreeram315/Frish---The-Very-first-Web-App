from django.db import models
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.shortcuts import redirect
# Create your models here.
from accounts.models import AccountInfo
from .utils import unique_slug_generator

User = settings.AUTH_USER_MODEL



class TweetInfo(models.Model):
	owner		=	models.ForeignKey(User, on_delete = 'CASCADE')
	content		=	models.CharField(max_length = 180, blank = True, null = True)
	date 		=	models.DateField(null = True, blank = True, auto_now_add = True)
	time 		=	models.TimeField(null = True, blank = True, auto_now_add = True)
	date_time 	=	models.DateTimeField(auto_now = True)
	tweet_count	=	models.IntegerField(null = True, blank = True)
	slug		=	models.SlugField(null = True, blank  = True)
	total_tweet_count = models.IntegerField(null = True, blank = True)

	def __str__(self):
		obj = AccountInfo.objects.get(owner = self.owner)
		return f'{obj.name}-{self.tweet_count}-{self.content[:15]}'

	@property
	def title(self):
		return self.content

# def prof_info_post_save(sender, instance, created, *args, **kwargs):
# 	if created:
# 		instance.name = 'nano'
# 		profile, is_created = AccountInfo.objects.get_or_create(owner = instance, name = instance, slug = instance, username = instance)


def tweet_pre_save(sender, instance, *args, **kwargs):
	print('saving')
	##### tweet_count
	try:
		last_tweet = TweetInfo.objects.filter(owner = instance.owner).latest('date_time')
		last_count = last_tweet.tweet_count
	except:
		last_count = 0
	instance.tweet_count = last_count + 1
	###### total_tweet_count
	try:
		last_tweet = TweetInfo.objects.all().latest('date_time')
		instance.total_tweet_count = last_tweet.tweet_count + 1
	except:
		instance.total_tweet_count = 1
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)


# pre_save.connect(pre_info_post_save, sender = User)
# post_save.connect(prof_info_post_save, sender = User)

pre_save.connect(tweet_pre_save, sender = TweetInfo)




