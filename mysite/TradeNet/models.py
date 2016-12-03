from __future__ import unicode_literals

from django.db import models

# Create your models here.
'''
class User (models.Model):
    userID = models.IntegerField(default=0) #Integer key for database
    balance = models.FloatField(default=0) #Float/real (only two decimal places allowed) for amount of money
    PnL = models.FloatField(default=0) #float/real total profit, negative value indicates loss
    portfolio = Portfolio() #Portfolio object to manage transactions and owned stock
'''

class Company(models.Model):
    name = models.CharField(max_length=200)
    finGrade = models.CharField(max_length=10)
    currentRev = models.FloatField(default=0)
    profit = models.FloatField(default=0)

class Stock(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=5)
    lastPrice = models.FloatField(default=0)
    exchange = models.FloatField(default=0)
    dailyNetChange = models.FloatField(default=0)

class Transaction(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    time = models.DateTimeField('time of transaction')
    quantity = models.IntegerField(default=1)
    buy = models.BooleanField(default=True)

class UserBalance(models.Model):
    email = models.CharField(max_length=200)
    balance = models.FloatField(default=0.00)
    profit = models.FloatField(default=0.00)

class OwnedStock(models.Model):
    user = models.ForeignKey(UserBalance, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)

class History(models.Model):
    user = models.ForeignKey(UserBalance, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)