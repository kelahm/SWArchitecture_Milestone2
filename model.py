class User:
    def __init__(self):
        self.userID = 0 #Integer key for database
        self.balance = 0 #Float/real (only two decimal places allowed) for amount of money
        self.PnL = 0 #float/real total profit, negative value indicates loss 
        self.portfolio = Portfolio() #Portfolio object to manage transactions and owned stock

    def buy(self, stockID, quantity):
        '''
        Returns boolean success/fail
        
        input:
        stockID - int database key
        quantity - int number to buy
        '''
        pass

    def sell(self, stockID, quantity):
        '''
        Returns boolean success/fail
        
        input:
        stockID - int database key
        quantity - int number to sell
        '''
        pass

    def addFunds(self, amount):
        '''
        returns boolean success/fail
        
        input:
        amount - float/real amount to add to balance
        '''
        pass
    
    def getBalance(self):
        '''
        returns float/real current balance
        '''
        pass

class Portfolio:
    def __init__(self):
        self.transactions = [] #List of transaction objects for history
        self.ownedStock = [] #List of stocks currently owned. INTENTIONALLY VIOLATES M1 CLASS DIAGRAM-must revise

    def addStock(self, stockID):
        '''
        returns boolean success/fail
        
        input:
        stockID - int database key
        '''
        pass

    def removeStock(self, stockID):
        '''
        returns boolean success/fail
        
        input:
        stockID - int database key
        '''
        pass

class Transaction:
    def __init__(self, stockID, price, time, quantity = 1):
        self.stock = Stock(stockID) #Stock object the transaction references
        self.price = price #Float/real price per stock that the transaction executed with
        self.time = time #Timestamp of when the transaction occured
        self.quantity = quantity #The amount of stock bought or sold

class Stock:
    def __init__(self, stockID = 0):
        pass

    def getCurrentPrice(self):
        '''
        returns float/real current price of the stock
        '''
        pass

class Company:
    def __init__(self, name, finGrade, currentRev, profit):
        pass

    def getName(self):
        '''
        returns string name
        '''
        pass

    def getFinGrade(self):
        '''
        returns char ('A', 'B', etc) financial grade for company
        '''
        pass

    def getCurrentRev(self):
        '''
        returns float/real current revenue of the company
        '''
        pass

    def getProfit(self):
        '''
        returns float/real current profit of the company
        '''
        pass
    
