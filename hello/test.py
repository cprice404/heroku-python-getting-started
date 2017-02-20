import os
import requests
from django.conf import settings

os.environ['DJANGO_SETTINGS_MODULE'] = 'gettingstarted.settings'
nation_slug = settings.NATIONBUILDER_SLUG
access_token = settings.NATIONBUILDER_ACCESS_TOKEN
url = "https://" + nation_slug + ".nationbuilder.com/api/v1/tags" + \
      "?access_token=" + access_token

r = requests.get(url, headers={'content-type': 'application/json'})
print map(lambda x: x['name'], r.json()['results'])
