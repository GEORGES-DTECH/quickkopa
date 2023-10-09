import requests

from requests.auth import HTTPBasicAuth

c2b_short_code = "600991"

# ===================GENERATING ACCESS TOKEN===================

consumer_key = "Sg8NX9NkOzcZT1QFK0IpExN1D5IfRm9r"
consumer_secret = "yaITtHBcS0Oge8rG"

api_url = (
    "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
)
result = requests.get(api_url, auth=HTTPBasicAuth(consumer_key,consumer_secret))
print(result)
json_response = result.json()
my_access_token = json_response["access_token"]
print(my_access_token)


def register_url():

    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"

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


# def c2b_payment():

#     api_url= "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
#     headers ={"Authorization":"Bearer %s"%  my_access_token }

#     request={
#             "ShortCode": c2b_short_code,
#             "CommandID":"CustomerPayBillOnline",
#              "Amount":"1000",
#             "Msisdn": "254708374149",
#             "BillRefNumber": "29388002",
#         }


#     response = requests.post(api_url,json=request,headers=headers,verify=False)


#     print(response.text)
# c2b_payment()
