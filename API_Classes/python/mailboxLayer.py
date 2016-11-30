import urllib2
import json


class MailboxLayer():
    def __init__(self, email):
        self.email = email
    
     

    def verifyEmail(self):
        api_key = '71becf10dd7d760ac81920b2103336d0'
        url = 'https://apilayer.net/api/check?access_key=' + api_key    #Build Request URL
        final_url = url +"&email="+ self.email 
        json_response = urllib2.urlopen(final_url)
        data = json.load(json_response)
       
       
        
        if data['format_valid'] == True and data['mx_found'] == True and data['smtp_check'] == True:
            return self.email + " is a valid email address."
        else:
            return self.email + " is not a valid email address."
            



                