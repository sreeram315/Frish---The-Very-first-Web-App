from django import forms

from .models import StudentInfo

class StudentAddForm(forms.Form):
	reg_no		=	forms.IntegerField()
	name		=	forms.CharField(required = False)
	cgpa		=	forms.FloatField()
	dob			=	forms.DateField()
	section		=	forms.CharField(required = False)
	contact		=	forms.IntegerField(required = False)
	batch		=	forms.IntegerField(required = False)
	address		=	forms.CharField(required = False)
	department	=	forms.CharField(required = False)
	updated		=	forms.DateTimeField(required = False)
	slug		=	forms.SlugField(required = False)
	description	=	forms.CharField(required = False)



class StudentInfoCreateForm(forms.ModelForm):
	class Meta:
		model = StudentInfo
		fields =  [
			'name', 'reg_no', 'cgpa', 'dob', 'section', 'contact', 'batch', 'address', 'department', 'description'
		]

	def clean_name(self):
		name = self.cleaned_data.get('name')
		if name == None or len(name) <= 2:
			raise forms.ValidationError('Not a valid name')
		return name