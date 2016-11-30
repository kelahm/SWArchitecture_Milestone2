from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.models import User
from ReCaptcha import *
from oauth2client import client, crypt

reCaptcha = ReCaptcha()
CLIENT_ID = '427104067013-l2kc1tkhgmc8ghtgmkkvf4494teqiq3q.apps.googleusercontent.com'
APPS_DOMAIN_NAME = 'http://localhost:8000/TradeNet/'

class IndexView(generic.TemplateView):
	template_name = 'TradeNet/index.html'
	
	def post(self, request, *args, **kwargs):
		m = User.objects.filter(username=request.POST['username'])
		if not m.exists():
			request.session['login_error'] = "invalid username"
		elif m[0].check_password(request.POST['password']):
			request.session['member_name'] = m[0].first_name
			context_object_name = 'latest_question_list'
			if 'login_error' in request.session:
				del request.session['login_error']
		else:
			request.session['login_error'] = "Invalid password"
		
		return render(request, self.template_name)
		
class CreateUserView(generic.TemplateView):
	template_name = 'TradeNet/create_user.html'
	
	def post(self, request, *args, **kwargs):
		if request.POST['password'] != request.POST['password2']:
			request.session['create_user_error'] = "Passwords do not match. Try again."
			return render(request, self.template_name)
		if reCaptcha.verify(request.POST['g-recaptcha-response']):
			new_user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
			new_user.last_name = request.POST['last_name']
			new_user.first_name = request.POST['first_name']
			new_user.save()
			request.session['member_name'] = new_user.first_name
			
			if 'create_user_error' in request.session:
				del request.session['create_user_error']
			return render(request, self.template_name)
		else:
			request.session['create_user_error'] = "ReCaptcha failed. Try again."
			return render(request, self.template_name)
		
def logout(request):
	del request.session['member_name']
	return HttpResponseRedirect(reverse('TradeNet:index'))
	
def tokensignin(request):
	token = request.POST['idtoken']
	try:
		idinfo = client.verify_id_token(token, CLIENT_ID)
		if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
			return HttpResponse("Wrong issuer")
	except (crypt.AppIdentityError):
		# Invalid token
		return HttpResponse("Invalid token")
	
	m = User.objects.filter(username=idinfo['email'])
	if not m.exists():
		new_user = User.objects.create_user(idinfo['email'], idinfo['email'], 'opinawefoinawlkn')
		new_user.last_name = idinfo['family_name']
		new_user.first_name = idinfo['given_name']
		new_user.save()
	request.session['member_name'] = idinfo['given_name']
	request.session['google_account'] = True
	return HttpResponse("ok")
