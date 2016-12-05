import httplib
import json

class TradierAPI():
	def getQuote(self, symbol):
		# Request: Market Quotes (https://sandbox.tradier.com/v1/markets/quotes?symbols=spy)
		connection = httplib.HTTPSConnection('sandbox.tradier.com', 443, timeout = 30)

		# Headers
		headers = {"Accept":"application/json",
					"Authorization":"Bearer vKfcXLeyeA3dss3ll6hN08SFuZUL"}

		# Send synchronously
		connection.request('GET', '/v1/markets/quotes?symbols='+symbol, None, headers)
		try:
			response = connection.getresponse()
			content = response.read()
			# Success

			parsed_json = json.loads(content)
          
		except httplib.HTTPException, e:
			# Exception
			print('Exception during request')
			parsed_json = False
		
		return parsed_json
		
		
	def search(self, term):
		# Request: Search for stocks (https://api.tradier.com/v1/markets/search?q=google)
		connection = httplib.HTTPSConnection('sandbox.tradier.com', 443, timeout = 30)

		# Headers
		headers = {"Accept":"application/json",
					"Authorization":"Bearer vKfcXLeyeA3dss3ll6hN08SFuZUL"}

		# Send synchronously
		connection.request('GET', '/v1/markets/search?q='+term, None, headers)
		try:
			response = connection.getresponse()
			content = response.read()
			# Success
          
			parsed_json = json.loads(content)
          
		except httplib.HTTPException, e:
			# Exception
			print('Exception during request')
			parsed_json = False

		return parsed_json
