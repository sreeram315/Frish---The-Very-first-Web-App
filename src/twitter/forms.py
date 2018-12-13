from django import forms

from .models import TweetInfo

class TwitterForm(forms.Form):
	content		=	forms.CharField(required = True)



class NewTweetForm(forms.ModelForm):
	class Meta:
		model = TweetInfo
		fields =  [
			'content'
		]

	def clean_content(self):
		content = self.cleaned_data.get('content')
		if content == None or len(content) <= 2:
			raise forms.ValidationError('Type somthing please')
		return content