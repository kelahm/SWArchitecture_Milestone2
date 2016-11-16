class User:
    def __init__(self):
        self.userID = 0
        self.balance = 0
        self.PnL = 0 #float/real total profit, negative value indicates loss 
        self.portfolio = Portfolio()

    def buy(self, stockID, quantity):
        pass

    def sell(self, stockID, quantity):
        pass

    def addFunds(self, amount):
        pass

class Portfolio:
    def __init__(self):
        self.transactions = []
        self.ownedStock = [] #INTENTIONALLY VIOLATES M1 CLASS DIAGRAM-must revise

    def addStock(self, stockID):
        pass

    def removeStock(self, stockID):
        pass

class Transaction:
    def __init__(self, stockID, price, time, quantity = 1):
        self.stock = Stock(stockID)
        self.price = price
        self.time = time
        self.quantity = quantity

class Stock:
    def __init__(self, stockID = 0):
        pass

    def getCurrentPrice(self):
        #Will return the current market value of the stock
        pass

class Company:
    def __init__(self):
        pass

    def getName(self):
        pass

    def getFinGrade(self):
        pass

    def getCurrentRev(self):
        pass

    def getProfit(self):
        pass
    
