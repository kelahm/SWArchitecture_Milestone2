from django.conf.urls import url

from . import views

app_name = 'TradeNet'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^portfolio', views.PortfolioView.as_view(), name='portfolio'),
	url(r'^addfunds', views.AddFundsView.as_view(), name='add_funds'),
	url(r'^withdrawalfunds', views.WithdrawalFundsView.as_view(), name='withdrawal_funds'),
	url(r'^transactionhistory', views.TransactionHistoryView.as_view(), name='transaction_history'),
	url(r'^createuser', views.CreateUserView.as_view(), name='create_user'),
	url(r'^logout', views.logout, name='logout'),
	url(r'^tokensignin', views.tokensignin, name='tokensignin'),
]
