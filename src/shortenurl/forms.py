from django import forms
from django.contrib.auth import get_user_model, authenticate, login
from django.core.exceptions import ValidationError
#
from .models import UrlInfo

User 	= get_user_model()

class CountForm(forms.Form):
	name				=	forms.CharField(required = False)
	original_link		=	forms.CharField(required = True)
	redirection_link	=	forms.CharField(required = False)


class CountUrlForm(forms.ModelForm):
	name				=	forms.CharField(label = 'You name(Optional)', required = False)
	original_link		=	forms.CharField(label = 'Original Link')
	redirection_link	=	forms.CharField(label = 'Redirect to(Optional):', required = False)

	class Meta:
		model = UrlInfo
		fields = ('name', 'original_link', 'redirection_link' )

	def clean_redirection_link(self):
		link 	=	self.cleaned_data.get('redirection_link')
		qs = UrlInfo.objects.filter(redirection_link__iexact = link)
		if qs.exists():
			raise ValidationError('link already in use, please choose another one leave this blank to let us do that for you.')
		return link


		
