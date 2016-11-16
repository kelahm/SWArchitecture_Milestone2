import httplib
import json

class TradierAPI():
    def __init__(self,symbol):
        self.symbol = symbol

    def request(self):

        # Request: Market Quotes (https://sandbox.tradier.com/v1/markets/quotes?symbols=spy)

        connection = httplib.HTTPSConnection('sandbox.tradier.com', 443, timeout = 30)

        # Headers

        headers = {"Accept":"application/json",
                   "Authorization":"Bearer vKfcXLeyeA3dss3ll6hN08SFuZUL"}

        # Send synchronously

        connection.request('GET', '/v1/markets/quotes?symbols='+self.symbol, None, headers)
        try:
          response = connection.getresponse()
          content = response.read()
          # Success
          
          parsed_json = json.loads(content)
          print("Current Price: " + str(parsed_json['quotes']['quote']['bid']))
          print("Change: " + str(parsed_json['quotes']['quote']['change']))
          print("Percent Change: " + str(parsed_json['quotes']['quote']['change_percentage']))
          print("Volume: " + str(parsed_json['quotes']['quote']['volume']))
          
        except httplib.HTTPException, e:
          # Exception
          print('Exception during request')
























##import urllib2
##
##def main():
##    req = urllib2.Request('https://api.tradier.com/v1/user/profile')
##    req.add_header('Authorization', 'Bearer')
##    f = urllib2.urlopen(req)
##    print f.read()
##
##if __name__ == '__main__':
##    main()
