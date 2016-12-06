from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.models import User
from TradeNet.models import History, UserBalance, Stock, Transaction, OwnedStock
from ReCaptcha import *
from mailboxLayer import *
from newsAPI import *
from TradierAPI import *
from oauth2client import client, crypt
from datetime import datetime
from twitter import *

reCaptcha = ReCaptcha()
mailboxLayer = MailboxLayer()
news = NewsApi()
trade = TradierAPI()
CLIENT_ID = '427104067013-l2kc1tkhgmc8ghtgmkkvf4494teqiq3q.apps.googleusercontent.com'
APPS_DOMAIN_NAME = 'http://localhost:8000/TradeNet/'
tweets = Twitter()

class IndexView(generic.TemplateView):
	template_name = 'TradeNet/index.html'
	
	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		context['articles'] = news.getNews()
		return context

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
		m = User.objects.filter(username=request.POST['username'])
		n = User.objects.filter(email=request.POST['email'])
		if request.POST['password'] != request.POST['password2']:
			request.session['create_user_error'] = "Passwords do not match. Try again."
			return render(request, self.template_name)
		if not mailboxLayer.verifyEmail(request.POST['email']):
			request.session['create_user_error'] = "Email is not valid. Try again."
			return render(request, self.template_name)
		if m.exists():
			request.session['create_user_error'] = "Username taken. Try again."
			return render(request, self.template_name)
		if n.exists():
			request.session['create_user_error'] = "Email is already registered. Do you already have an acount?"
			return render(request, self.template_name)
		if reCaptcha.verify(request.POST['g-recaptcha-response']):
			new_user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
			user_balance = UserBalance(email=request.POST['email'])
			new_user.last_name = request.POST['last_name']
			new_user.first_name = request.POST['first_name']
			new_user.save()
			user_balance.save()
			request.session['member_name'] = new_user.first_name
			request.session['member_email'] = new_user.email
			
			if 'create_user_error' in request.session:
				del request.session['create_user_error']
			return render(request, self.template_name)
		else:
			request.session['create_user_error'] = "ReCaptcha failed. Try again."
			return render(request, self.template_name)

class PortfolioView(generic.TemplateView):
	template_name = 'TradeNet/portfolio.html'
	
	def get_context_data(self, **kwargs):
		context = super(PortfolioView, self).get_context_data(**kwargs)
		user = UserBalance.objects.get(email=self.request.session['member_email'])
		context['user_balance'] = user
		shares = OwnedStock.objects.filter(user__email=self.request.session['member_email'])
		if shares.exists():
			context['stocks'] = shares
		else:
			context['stocks'] = None
		return context

	def post(self, request, *args, **kwargs):
		user = UserBalance.objects.get(email=self.request.session['member_email'])
		if request.POST['update'] == "add":
			user.balance += float(request.POST['funds'])
			user.save()
			context = self.get_context_data(**kwargs)
			context['message'] = "Funds have been added"
		else:
			user.balance -= float(request.POST['funds'])
			user.save()
			context = self.get_context_data(**kwargs)
			context['message'] = "Funds have been removed"
		return render(request, self.template_name, context)
		
class AddFundsView(generic.TemplateView):
	template_name = 'TradeNet/addfunds.html'

class WithdrawalFundsView(generic.TemplateView):
	template_name = 'TradeNet/withdrawalfunds.html'
	
class TransactionHistoryView(generic.TemplateView):
	template_name = 'TradeNet/transactionhistory.html'
	
	def get_context_data(self, **kwargs):
		context = super(TransactionHistoryView, self).get_context_data(**kwargs)
		transactions = History.objects.filter(user__email=self.request.session['member_email'])
		if transactions.exists():
			context['transactions'] = transactions
		else:
			context['transactions'] = None
		return context
			
class BuySellView(generic.TemplateView):
	template_name = 'TradeNet/buysell.html'
	
	def get_context_data(self, **kwargs):
		context = super(BuySellView, self).get_context_data(**kwargs)
		context['symbol'] = kwargs['symbol']
		context['action'] = kwargs['action']
		results=trade.getQuote(kwargs['symbol'])
		if results:
			context['quote_results'] = results
			context['size'] = len(results['quotes'])
		else:
			context['message'] = "Stock not found"
			
		if kwargs['action'] == 'sell':
			owned_stock = OwnedStock.objects.filter(user__email=self.request.session['member_email'])
			if owned_stock.exists():
				context['count'] = owned_stock[0].quantity
			else:
				context['count'] = 0
		return context

	def post(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		results=trade.getQuote(kwargs['symbol'])
		s_user = UserBalance.objects.get(email=self.request.session['member_email'])
		total = float(request.POST['count']) * float(results['quotes']['quote']['last'])
		if request.POST['update'] == "buy":
			if s_user.balance > total:
				search_stock = Stock.objects.filter(ticker=results['quotes']['quote']['symbol'])
				if search_stock.exists():
					s_stock = search_stock[0]
					s_stock.lastPrice=float(results['quotes']['quote']['last'])
					s_stock.dailyNetChange=float(results['quotes']['quote']['change'])
				else:
					s_stock = Stock(company=results['quotes']['quote']['description'],ticker=results['quotes']['quote']['symbol'],lastPrice=float(results['quotes']['quote']['last']),exchange=results['quotes']['quote']['exch'],dailyNetChange=float(results['quotes']['quote']['change']))
				
				s_stock.save()
				s_transaction = Transaction(stock=s_stock,price=float(results['quotes']['quote']['last']),time=datetime.utcnow(),quantity=int(request.POST['count']),buy=True)
				s_transaction.save()
				owned_stock = OwnedStock.objects.filter(user__email=self.request.session['member_email'],stock=s_stock)
				if owned_stock.exists():
					s_owned_stock = owned_stock[0]
					s_owned_stock.quantity += int(request.POST['count'])
					s_owned_stock.save()
				else:
					s_owned_stock = OwnedStock(user=s_user,stock=s_stock,quantity=int(request.POST['count']),transaction=s_transaction)
					s_owned_stock.save()
				
				s_user.balance -= total
				s_user.save()
				history = History(user=s_user,transaction=s_transaction)
				history.save()
				context['message'] = "Stocks have been bought"
			else:
				context['message'] = "You do not have enough money in your account to pay for the stocks"
			
		else:
			search_stock = Stock.objects.filter(ticker=results['quotes']['quote']['symbol'])
			if not search_stock.exists():
				context['message'] = "You do not own this stock"
				return render(request, self.template_name, context)
			s_stock = search_stock[0]
			s_owned_stock = OwnedStock.objects.filter(user__email=self.request.session['member_email'], stock=s_stock)
			if not s_owned_stock.exists():
				context['message'] = "You do not own this stock"
				return render(request, self.template_name, context)
			owned_stock = s_owned_stock[0]
			if owned_stock.quantity >= int(request.POST['count']):
				s_stock.lastPrice=float(results['quotes']['quote']['last'])
				s_stock.dailyNetChange=results['quotes']['quote']['change']
				s_stock.save()
				s_transaction = Transaction(stock=s_stock,price=float(results['quotes']['quote']['last']),time=datetime.utcnow(),quantity=int(request.POST['count']),buy=False)
				s_transaction.save()
				
				owned_stock.quantity -= int(request.POST['count'])
				if owned_stock.quantity == 0:
					owned_stock.delete()
				else:
					owned_stock.save()
					
				difference = float(results['quotes']['quote']['last']) - owned_stock.transaction.price
				s_user.profit += (difference*float(request.POST['count']))
				s_user.balance += total
				s_user.save()
				history = History(user=s_user,transaction=s_transaction)
				history.save()
				context['message'] = "Stocks have been sold"
			else:
				context['message'] = "You do not have that many stocks to sell"
		return render(request, self.template_name, context)

class StocksView(generic.TemplateView):
	template_name = 'TradeNet/stocks.html'
	
	def get_context_data(self, **kwargs):
		context = super(StocksView, self).get_context_data(**kwargs)
		return context

	def post(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		results=trade.search(request.POST['term'])
		if results:
			context['search_results'] = results
			if 'symbol' in results['securities']['security']:
				context['size'] = 1
			else:
				context['size'] = len(results['securities']['security'])
		else:
			context['message'] = "Search failed"
		return render(request, self.template_name, context)			
				
class DetailsView(generic.TemplateView):
	template_name = 'TradeNet/details.html'
	
	def get_context_data(self, **kwargs):
		context = super(DetailsView, self).get_context_data(**kwargs)
		results=trade.getQuote(kwargs['symbol'])
		if results:
			context['quote_results'] = results
			context['size'] = len(results['quotes'])
		else:
			context['message'] = "Stock not found"
			
		result=tweets.search(kwargs['symbol'])
		if result:
			context['tweet_results'] = result
		else:
			context['message'] = "Tweets not found"

		return context

def logout(request):
	del request.session['member_name']
	del request.session['member_email']
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
