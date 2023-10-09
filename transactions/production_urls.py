import requests

from requests.auth import HTTPBasicAuth

c2b_short_code = "6384792"

consumer_key = "jINVfIREGlvrRZSERArWP0ldGfWIGoxv"
consumer_secret = "tCvh1XMdPbV3H6VI"

api_url = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
result = requests.get(api_url,auth=HTTPBasicAuth(consumer_key,consumer_secret))

json_response = result.json()
my_access_token = json_response["access_token"]
print(my_access_token)



def register_url():

    api_url = "https://api.safaricom.co.ke/mpesa/c2b/v2/registerurl"
    headers = {"Authorization": "Bearer %s" % my_access_token}
    request = {
        "ShortCode": c2b_short_code,
        "ResponseType": "Completed",
        "ConfirmationURL": "https://timeline.repotranstech.com/confirmation/",
        "ValidationURL": "https://timeline.repotranstech.com/validation/",
       
    }

    response = requests.post(api_url, json=request, headers=headers)

    print(response.text)


register_url()

