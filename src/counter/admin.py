from django.contrib import admin

# Register your models here.

from .models import CountInfo, CountUpdateInfo

admin.site.register(CountInfo)
admin.site.register(CountUpdateInfo)
