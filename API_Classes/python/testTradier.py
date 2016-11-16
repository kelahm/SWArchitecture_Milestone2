from TradierAPI import TradierAPI

print("Google")
t=TradierAPI("GOOG")
t.request()

print("")

print("Apple")
t1=TradierAPI("AAPL")
t1.request()

print("")

print("Microsoft")
t2=TradierAPI("MSFT")
t2.request()
