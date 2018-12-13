from django.db import models
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.db.models import Q


# Create your models here.

from .utils import unique_slug_generator
from .validators import validate_section

User = settings.AUTH_USER_MODEL

class StudentInfoManager(models.Manager):
	# def search(self, query, user, reverse = False, sort_by = 'name', top_n = 100, gender_select = None, state_select = None):
	# 	query = query.strip()
	# 	if not state_select or state_select == 'ALL':
	# 		qs =  self.get_queryset().filter(
	# 						Q(name__icontains = query)|
	# 						Q(reg_no__icontains = query)|
	# 						Q(batch__iexact = query)|
	# 						Q(section__iexact = query),
	# 						gender__in = list(gender_select),
							
	# 						owner = user
	# 					).order_by(sort_by)
	# 	else:
	# 		qs =  self.get_queryset().filter(
	# 						Q(name__icontains = query)|
	# 						Q(reg_no__icontains = query)|
	# 						Q(batch__iexact = query)|
	# 						Q(section__iexact = query),
	# 						gender__in = list(gender_select),
	# 						state__icontains = state_select,
	# 						owner = user
	# 					).order_by(sort_by)
	# 	count	=	qs.count()
	# 	if reverse: return qs.reverse()[:top_n], count
	# 	return qs[:top_n], count

	def search(self, user, query='', order_by='name', reverse=False, gender_select = 'MF', state_select='', top_n=100):
			qs = self.get_queryset().filter(Q(name__icontains = query) 	 		|
											Q(reg_no__icontains = query) 		|
											Q(batch__icontains = query) 		|
											Q(section__icontains = query)		,
											Q(state__icontains = state_select)  | Q(state__in = state_select)   ,
											gender__in	=	gender_select,
											owner = user
							).order_by(
											order_by
							)


			if reverse: return qs.reverse()[:top_n], qs.count()
			return qs[:top_n], qs.count()


				

																


class StudentInfo(models.Model):
	owner		=	models.ForeignKey(User, on_delete = 'CASCADE')
	reg_no		=	models.IntegerField()
	name		=	models.CharField(max_length = 300, null = True, blank = True)
	cgpa		=	models.FloatField(null = True, blank  = True)
	dob			=	models.DateField(null = True, blank  = True)
	gender		=	models.CharField(max_length = 1, null = True, blank = True)
	section		=	models.CharField(max_length = 100, null = True, blank = True, validators = [validate_section])
	contact		=	models.CharField(max_length = 100, null = True, blank = True)
	batch		=	models.IntegerField(null = True, blank  = True)
	address		=	models.CharField(max_length = 1000, null = True, blank = True)
	department	=	models.CharField(max_length = 300, null = True, blank = True)
	updated		=	models.DateTimeField(auto_now = True, null = True, blank = True)
	slug		=	models.SlugField(null = True, blank  = True)
	state		=	models.CharField(max_length = 200, null = True, blank = True)
	description	=	models.CharField(max_length = 9999, blank = True, null = True)

	#class Meta:
		#ordering = ['-updated']

	objects = StudentInfoManager()

	def __str__(self):
		return str(self.name)

	@property
	def title(self):
		return self.name



def stu_info_pre_save(sender, instance, *args, **kwargs):
	print('saving')
	state = '--'
	try:
		state = instance.address.split()[-2]
		if state == '-': state = instance.address.split()[-3]

		if state == 'Pradesh': state = instance.address.split()[-3] + ' ' + state
		elif state == 'Kashmir': state = 'Jammu & kashmir'
		elif state == 'Nadu': state = 'Tamil Nadu'
		elif state == 'Bengal': state = 'West Bengal'
		else: state = instance.address.split()[-2]
	except: pass
	instance.state = state
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)

pre_save.connect(stu_info_pre_save, sender = StudentInfo)
	

