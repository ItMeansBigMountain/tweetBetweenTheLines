import requests
import base64
import json





# GLOBAL VARIABLES
consumer_key = "" 
consumer_secret = ""
access_key = ""
access_secret = ""

bearer_token = ""






#ENCODING (b64_encoded_key)
key_secret = '{}:{}'.format(consumer_key, consumer_secret).encode('ascii')
b64_encoded_key = base64.b64encode(key_secret)
b64_encoded_key = b64_encoded_key.decode('ascii')


# AUTH REQUEST (access_token)
base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)
auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}
auth_data = {
    'grant_type': 'client_credentials'
}
auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
access_token = auth_resp.json()['access_token']










# USAGE REQUEST


# TRENDS
trend_headers = {
    'Authorization': 'Bearer {}'.format(access_token)    
}
trend_params = {
    # GLOBAL
    'id': 1,
    # "Where on earth ID" of locations found on https://www.findmecity.com/
    # 'id': 2379574,  #chicago
    # 'id': 23424922,  #pakistan
}
trend_url = 'https://api.twitter.com/1.1/trends/place.json'  
trend_resp = requests.get(trend_url, headers=trend_headers, params=trend_params).json()






# OUTPUT SAVE TO JSON FILE
with open("test.json", "w") as f:
    json.dump(trend_resp, f)


