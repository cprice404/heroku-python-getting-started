from django.shortcuts import render
from django.conf import settings
# from django.http import HttpResponse
import requests

from .models import Greeting

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')

    # response = session.get("https://" + nation_slug + ".nationbuilder.com/api/v1/tags" +
    #     "?access_token=" + access_token + "limit=10")
    #
    # params={'format': 'json'}
    # headers={'content-type': 'application/json'}

    nation_slug = settings.NATIONBUILDER_SLUG
    access_token = settings.NATIONBUILDER_ACCESS_TOKEN
    url = "https://" + nation_slug + ".nationbuilder.com/api/v1/tags" + \
          "?access_token=" + access_token

    r = requests.get(url, headers={'content-type': 'application/json'})
    tags = map(lambda x: x['name'], r.json()['results'])
    return render(request, 'index.html', context={'tags': tags})


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

