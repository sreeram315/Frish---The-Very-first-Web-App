from django import forms

from .models import AccountInfo
from django.contrib.auth import get_user_model, authenticate, login
from django.core.exceptions import ValidationError


User 	= get_user_model()

class AccountForm(forms.Form):
	name		=	forms.CharField(required = False)
	dob			=	forms.DateField()
	contact		=	forms.IntegerField(required = False)
	address		=	forms.CharField(required = False)
	updated		=	forms.DateTimeField(required = False)
	description	=	forms.CharField(required = False)


class RegisterForm(forms.ModelForm):
	name	= forms.CharField(label = 'Full name', required = False)
	pass1 	= forms.CharField(label = 'Password', widget = forms.PasswordInput)
	pass2 	= forms.CharField(label = 'Password confirmation', widget = forms.PasswordInput)


	class Meta:
		model = User
		fields = ('name', 'username' ,'email',)

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if len(email) < 2: raise ValidationError('Enter Valid email address')
		qs = User.objects.filter(email = email)
		if qs.exists():
			raise ValidationError('Email already in use')
		return email

	def clean_pass2(self):
		pass1 = self.cleaned_data.get('pass1')
		pass2 = self.cleaned_data.get('pass2')
		if pass1 and pass2 and pass1 != pass2:
			raise ValidationError('paswords don\'t match')
		return pass2

	def save(self, commit = True):
		user = super(RegisterForm, self).save(commit = False)
		user.set_password(self.cleaned_data['pass1'])
		if commit:
			user.save()
			#user.accountinfo.send_activation_email()
			username = self.cleaned_data.get('username')
			password = self.cleaned_data.get('pass1')
			user.accountinfo.login_re(username, password)
		return user




