from django.shortcuts import render, redirect
from django.conf import settings
from rauth import OAuth2Service
import json
import sys

class Cache:
    tokens = {}

# Create your views here.
def index(request):
    return render(request, 'index.html')

def nation_login(request):
    nation_slug = request.POST.get('nation_slug')
    request.session['nation_slug'] = nation_slug

    url = get_redirect_url(nation_slug)
    return redirect(url)

def oauth_callback(request):
    oauth_code = request.GET.get('code')

    nation_slug = request.session['nation_slug']
    service = get_oauth_service(nation_slug)
    redirect_uri = settings.NATIONBUILDER_APP_OAUTH_CALLBACK
    token = service.get_access_token(decoder=json.loads,
                                     data={"code": oauth_code,
                                           "redirect_uri": redirect_uri,
                                           "grant_type": "authorization_code"})

    Cache.tokens[request.session.session_key] = token
    return tags(request)

def tags(request):
    tag_prefix = request.POST.get('tag_prefix')

    nation_slug = request.session['nation_slug']
    service = get_oauth_service(nation_slug)
    token = Cache.tokens[request.session.session_key]
    session = service.get_session(token)

    response = session.get("https://"+nation_slug+".nationbuilder.com/api/v1/tags?limit=1000",
                           params={'format': 'json'},
                           headers={'content-type': 'application/json'})
    tags = map(lambda x: x['name'], response.json()['results'])

    filtered_tags = []
    if tag_prefix:
        filtered_tags = filter(lambda x: x.lower().startswith(tag_prefix.lower()),
                               tags)

    matching_people = []
    filtered_tag_index = 0
    while (len(matching_people) < 10) and (filtered_tag_index < len(filtered_tags)):
        url = "https://" + nation_slug +\
            ".nationbuilder.com/api/v1/tags/" +\
            filtered_tags[filtered_tag_index] +\
            "/people"
        print("REQUESTING PEOPLE FROM URL: " + url)
        sys.stdout.flush()
        people_response = session.get(url,
                                      params={'format': 'json'},
                                      headers={'content-type': 'application/json'})
        people = people_response.json()['results']
        for person in people:
            matching_people.append(person['first_name'] + " " + person['last_name'])
        filtered_tag_index += 1

    return render(request, 'tags.html', context={'tags': tags,
                                                 'tag_prefix': tag_prefix or '',
                                                 'filtered_tags': filtered_tags,
                                                 'matching_people': matching_people})

# def db(request):
#
#     greeting = Greeting()
#     greeting.save()
#
#     greetings = Greeting.objects.all()
#
#     return render(request, 'db.html', {'greetings': greetings})

def get_redirect_url(nation_slug):
    client_id = settings.NATIONBUILDER_APP_CLIENT_ID
    redirect_uri = settings.NATIONBUILDER_APP_OAUTH_CALLBACK

    return 'https://' + nation_slug + \
        '.nationbuilder.com/oauth/authorize?response_type=code' + \
        '&client_id=' + client_id + \
        '&redirect_uri=' + redirect_uri

def get_oauth_service(nation_slug):
    client_id = settings.NATIONBUILDER_APP_CLIENT_ID
    client_secret = settings.NATIONBUILDER_APP_CLIENT_SECRET

    service = OAuth2Service(
            client_id=client_id,
            client_secret=client_secret,
            name='oauth_name',
            authorize_url="https://" + nation_slug + ".nationbuilder.com/oauth/authorize",
            access_token_url="https://" + nation_slug + ".nationbuilder.com/oauth/token",
            base_url="https://" + nation_slug + ".nationbuilder.com")
    return service