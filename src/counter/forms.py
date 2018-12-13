from django import forms

from .models import CountInfo
from django.contrib.auth import get_user_model, authenticate, login
from django.core.exceptions import ValidationError


User 	= get_user_model()

class CountForm(forms.Form):
	creater	=	forms.CharField(required = True)
	name 	=	forms.CharField(required = True)
	slug	=	forms.SlugField(required = True)


class CounterCreateForm(forms.ModelForm):
	class Meta:
		model = CountInfo
		fields = ['creater', 'name']

	def clean_name(self):
		name = self.cleaned_data.get('name')
		qs = CountInfo.objects.filter(name__iexact = name)
		if qs.exists():
			raise ValidationError('Name already in use')
		return name

