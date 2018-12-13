from django.conf.urls import url
from django.contrib import admin
from .views import (ContactTView, StudentLView, StudentDetails, StudentInfoCreateView, 
                    StudentInfoSection, StudentInfoUpdateView, UploadStudentDetails)
from django.views.generic import TemplateView



urlpatterns = [
    url(r'^students_list/(?P<reg_id>\d*)$', StudentLView.as_view(), name = 'students-list'),
    url(r'^details/(?P<slug>[\w-]+)$', StudentDetails.as_view(), name = 'students-details'),
    url(r'^add-new/$', StudentInfoCreateView.as_view(), name = 'students-add-new'),
    url(r'^(?P<pk>\d*)/update$', StudentInfoUpdateView.as_view(), name = 'students-update'),
    url(r'^filter-section/(?P<sect>[\w-]+)$', StudentInfoSection.as_view(), name = 'students-filter-section'),
    
    url(r'^upload-stu-details/$', UploadStudentDetails.as_view(), name = 'students-upload'),
]
