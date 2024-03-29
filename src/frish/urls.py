"""frish URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from students.views import ContactTView, StudentLView, StudentDetails, StudentInfoCreateView
from shortenurl.views import RedirectUrl
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', LoginView.as_view(), name = 'login'),
    url(r'^logout/', LogoutView.as_view(), name = 'logout'),
    url(r'^$', TemplateView.as_view(template_name = 'home.html'), name = 'home'),
    url(r'^about/$', TemplateView.as_view(template_name = 'about.html'), name = 'about'),
    url(r'^contact/(?P<reg_id>\d*)/$', ContactTView.as_view(), name = 'contact'),
    url(r'^counter/', include('counter.urls')),
    url(r'^students/', include('students.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^twitter/', include('twitter.urls')),
    url(r'^shortenurl/', include('shortenurl.urls')),
    url(r'^su/(?P<rlink>[\w-]*)/$', RedirectUrl.as_view(), name = 'contact'),

]
