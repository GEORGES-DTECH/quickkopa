from django.conf import settings
import requests
# AT_API_KEY ="c8de4182a10f40e0037ebef7ee1153d4aa061cde1a2094ce7a8f8065bd434724"
# AT_USERNAME = "sandbox"
# AT_FROM_VALUE = "6811"
# AT_ENDPOINT_URL = "https://api.sandbox.africastalking.com/version1/messaging"
# recipients = ["+254727574812"]

# shortcode= "6811"
# import requests

# url = "https://api.sandbox.africastalking.com/version1/messaging"

# headers = {'ApiKey': AT_API_KEY, 
#            'Content-Type': 'application/x-www-form-urlencoded',
#            'Accept': 'application/json'}


# data  = {'username': 'sandbox',
#         'from': shortcode,
#         'message': "hey hey",
#         'to': recipients}


# def make_post_request():  
#     response = requests.post( url = url, headers = headers, data = data )
#     return response


# print( make_post_request().json() )




def make_post_request():
        
        AT_API_KEY ="c8de4182a10f40e0037ebef7ee1153d4aa061cde1a2094ce7a8f8065bd434724"
        AT_USERNAME = "sandbox"
        AT_FROM_VALUE = "6811"
        recipients = ["+254727574812"]
        shortcode= "6811"
        url = "https://api.sandbox.africastalking.com/version1/messaging"

        headers = {'ApiKey': AT_API_KEY, 
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'}
    
        data  = {'username': AT_USERNAME,
            'from': AT_FROM_VALUE,
            'message': "hey hey welcome agian",
            'to': recipients}  
        response = requests.post( url = url, headers = headers, data = data )
        print(response)
        # return response
make_post_request()
    