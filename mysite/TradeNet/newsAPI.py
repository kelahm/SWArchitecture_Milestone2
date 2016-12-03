import urllib2
import json

class NewsApi():
    def __init__(self):
        self.api_key = 'bd0924d63c72470eb3db758fcdef2dce'

    def getNews(self):
        url = 'https://newsapi.org/v1/articles?source=business-insider&sortBy=top&apiKey=' + self.api_key
        json_response = urllib2.urlopen(url)
        data = json.load(json_response)

        return data