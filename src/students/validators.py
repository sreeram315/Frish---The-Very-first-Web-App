from django.core.exceptions import ValidationError
import re

def validate_section(value):
	if not bool(re.match(r'[a-zA-Z]{1,3}\d+$', value)):
		raise ValidationError('Not a valid section')