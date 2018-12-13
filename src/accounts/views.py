from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, View
from django.db.models import Q
# from django.views.generic.edit import UpdateView

# Create your views here.
from .forms import RegisterForm
from .models import AccountInfo
User =	get_user_model()




class AccountProfileView(LoginRequiredMixin,DetailView):
	template_name = 'accounts/profile.html'
	login_url	=	'/login/'

	def get_object(self):
		return get_object_or_404(AccountInfo, owner = self.request.user)


	# def get_queryset(self):
	# 	queryset = AccountInfo.objects.filter(owner = self.request.user)
	# 	print(queryset)
	# 	return queryset


	# def get_context_data(self, *args, **kwargs):
	# 	context = super(AccountInfo, self).get_context_data(*args, **kwargs)
	# 	return context

class AccountUpdateView(LoginRequiredMixin,UpdateView):
	login_url	=	'/login/'
	template_name = 'accounts/form.html'
	model = AccountInfo
	fields = ['name', 'email', 'dob', 'contact', 'address', 'slug', 'description']

	def get_success_url(self):
		return f'/accounts/profile/'

	def get_context_data(self, *args, **kwargs):
		context = super(AccountUpdateView, self).get_context_data(*args, **kwargs)
		context['title']	=	'Update Account'
		print(context)
		return context

class AccountOpenProfileView(LoginRequiredMixin,DetailView):
	login_url	=	'/login/'
	template_name = 'accounts/open_prof_view.html'
	
	def get_queryset(self, *args, **kwargs):
		slug = self.kwargs.get('slug')
		queryset = AccountInfo.objects.filter(slug = slug)
		return queryset

	def get_context_data(self, *args, **kwargs):
		context 	= super(AccountOpenProfileView, self).get_context_data(*args, **kwargs)
		slug 		= self.kwargs.get('slug')
		fing 		= AccountInfo.objects.get(slug = slug)
		user_ 		= self.request.user
		fler		= AccountInfo.objects.get(owner = user_)
		if fler.owner in fing.followers.all():
			context['is_following'] = True
		else:
			context['is_following'] = False
		return context

class AccountFollowToggle(LoginRequiredMixin,View):
	login_url	=	'/login/'
	def post(self, request,  *args, **kwargs):
		user_to_toggle	=	request.POST.get("username")
		profile_	=		AccountInfo.objects.get(username__iexact = user_to_toggle)
		user_1 = request.user
		AccountInfo.objects.toggle_follow(user_1, profile_)
		# if user not in profile_.followers.all():
		# 	profile_.followers.add(user)
		# else:
		# 	profile_.followers.remove(user)
		return redirect(f'/accounts/{profile_.slug}')

class AccountListView(LoginRequiredMixin,  ListView):
	template_name = 'accounts/list_view.html'
	login_url	=	'/login/'

	def get_queryset(self):
		search_query	=	self.request.GET.get('q')
		if search_query:
			qs = AccountInfo.objects.filter(Q(name__icontains = search_query)|
												Q(username__icontains = search_query)|
												Q(email__icontains = search_query))
			print(qs)
			return qs

		return AccountInfo.objects.all()

	def get_context_data(self, *args, **kwargs):
		context = super(AccountListView, self).get_context_data(*args, **kwargs)
		return context

class RegisterAccount(CreateView):
	form_class = RegisterForm
	template_name = 'accounts/register.html'
	success_url = '/'

	def get_success_url(self):
		user = authenticate(username = self.username , password = self.password)
		login(self.request, user)
		s = AccountInfo.objects.get(owner = self.request.user).slug
		print(s)
		return f'/accounts/{s}/update'
		

	def form_valid(self, form):
		form.save()
		self.username = form.cleaned_data['username']
		self.password = form.cleaned_data['pass1']
		return super(RegisterAccount, self).form_valid(form)

	def dispatch(self , *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect('/accounts/profile/')
		return super(RegisterAccount, self).dispatch(*args, **kwargs)


# class StudentInfoUpdateView(LoginRequiredMixin, UpdateView):
# 	template_name = 'students/add_new.html'
# 	model = StudentInfo
# 	fields = ['name', 'reg_no', 'cgpa', 'dob', 'section', 'contact', 'batch', 'address', 'department', 'description']
# 	login_url	=	'/login/'
# 	# success_url = f'/students/details/{slug}'

# 	def get_success_url(self):
# 		obj = StudentInfo.objects.get(pk=self.kwargs['pk'])
# 		return f'/students/details/{obj.slug}'

# 	def get_context_data(self, *args, **kwargs):
# 		context = super(StudentInfoUpdateView, self).get_context_data(*args, **kwargs)
# 		context['title']	=	'Update Item'
# 		return context
