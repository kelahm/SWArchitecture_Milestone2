import urllib2
import json

class NewsApi():
    def __init__(self):
        self.api_key = 'bd0924d63c72470eb3db758fcdef2dce'


    def getNews(self):
        url = 'https://newsapi.org/v1/sources?language=en&category=business&country=us&apiKey='+ self.api_key
        json_response = urllib2.urlopen(url)
        data = json.load(json_response)

    
        for item in data['sources']:
            print "Source: " + str(item['name']) +'\n'
            print "Description: " + str(item['description']) +'\n'
            print "URL: "+ str(item['url']) +'\n'
            print "Country: "+ str(item['country']) +'\n'
            print " "


