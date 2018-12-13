from django.db import models
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.db.models import Q


# Create your models here.

from .utils import unique_slug_generator


User = settings.AUTH_USER_MODEL

class UrlInfo(models.Model):
	name				=	models.CharField(max_length = 100, null = True, blank = True)
	original_link		=	models.CharField(max_length = 1000, null = True, blank = True)
	redirection_link	=	models.CharField(max_length = 100, null = True, blank = True)
	date_time			=	models.DateTimeField(auto_now = True, null = True, blank = True)



	def __str__(self):
		return str(self.original_link)

	@property
	def title(self):
		return self.original_link


	def get_absolute_url(self):
		return f'/shortenurl/success/{self.redirection_link}'



def stu_info_pre_save(sender, instance, *args, **kwargs):
	if not instance.redirection_link:
		instance.redirection_link	=	unique_slug_generator(instance)

pre_save.connect(stu_info_pre_save, sender = UrlInfo)
	

