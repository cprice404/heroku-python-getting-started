import os
import requests
from django.conf import settings
from rauth import OAuth2Service
import json

os.environ['DJANGO_SETTINGS_MODULE'] = 'gettingstarted.settings'


# nation_slug = settings.NATIONBUILDER_SLUG
# access_token = settings.NATIONBUILDER_ACCESS_TOKEN
# url = "https://" + nation_slug + ".nationbuilder.com/api/v1/tags" + \
#       "?access_token=" + access_token
#
# r = requests.get(url, headers={'content-type': 'application/json'})
# print map(lambda x: x['name'], r.json()['results'])

nation_slug = 'cprice404'
client_id = settings.NATIONBUILDER_APP_CLIENT_ID
redirect_uri = settings.NATIONBUILDER_APP_OAUTH_CALLBACK
client_secret = settings.NATIONBUILDER_APP_CLIENT_ID
oauth_code = 'c1c06f81a72c331f259fcbc198bf'

service = OAuth2Service(
        client_id=client_id,
        client_secret=client_secret,
        name='oauth_name',
        authorize_url="https://" + nation_slug + ".nationbuilder.com/oauth/authorize",
        access_token_url="https://" + nation_slug + ".nationbuilder.com/oauth/token",
        base_url="https://" + nation_slug + ".nationbuilder.com")

# token = service.get_access_token(decoder=json.loads,
#                                  data={"code": oauth_code,
#                                        "redirect_uri": redirect_uri,
#                                        "grant_type": "authorization_code"})

token = os.environ.get('NATIONBUILDER_DEV_TOKEN')

print("TOKEN: " + token)

#
# Get API session using token
#

session = service.get_session(token)

#
# Get API data using session
#
# response = session.get("https://"+nation_slug+".nationbuilder.com/api/v1/tags",
#                        params={'format': 'json'},
#                        headers={'content-type': 'application/json'})
# print("RESPONSE CLASS: " + str(response.__class__))
# print("RESPONSE:" + str(response))

# response = session.get("https://cprice404.nationbuilder.com/api/v1/tags/IMS DB/DC/people",
# response = session.get("https://cprice404.nationbuilder.com/api/v1/tags/IMS%20DB%2FDC/people",
response = session.get("https://cprice404.nationbuilder.com/api/v1/tags/Erwin/people",
                       params={'format': 'json'},
                       headers={'content-type': 'application/json'})
print("RESPONSE:" + str(response))
