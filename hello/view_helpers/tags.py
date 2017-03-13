import urllib

from django.shortcuts import render
from hello.utils.oauth import get_oauth_service


def handle_tags_request(request):
    tag_prefix = None
    selected_tag = None
    if request.method == 'POST':
        tag_prefix = request.POST.get('tag_prefix')
    elif request.method == 'GET':
        tag_prefix = request.GET.get('tag_prefix')
        selected_tag = request.GET.get('selected_tag')

    nation_slug = request.session['nation_slug']
    service = get_oauth_service(nation_slug)
    token = request.session['token']
    session = service.get_session(token)

    response = session.get("https://"+nation_slug+".nationbuilder.com/api/v1/tags?limit=1000",
                           params={'format': 'json'},
                           headers={'content-type': 'application/json'})
    tags = map(lambda x: x['name'], response.json()['results'])

    filtered_tags = []
    if tag_prefix:
        def to_tag_dict(tag):
            return {'raw': tag, 'encoded': urllib.quote_plus(tag)}

        filtered_tags = map(to_tag_dict,
                            filter(lambda x: x.lower().startswith(tag_prefix.lower()),
                                   tags))

    matching_people = []
    if selected_tag:
        url = "https://" + nation_slug + \
              ".nationbuilder.com/api/v1/tags/" + \
              selected_tag + \
              "/people"
        people_response = session.get(url,
                                      params={'format': 'json'},
                                      headers={'content-type': 'application/json'})
        people = people_response.json()['results']
        for person in people:
            matching_people.append(person['first_name'] + " " + person['last_name'])

    return render(request, 'tags.html', context={'tags': tags,
                                                 'tag_prefix': tag_prefix or '',
                                                 'filtered_tags': filtered_tags,
                                                 'selected_tag': selected_tag,
                                                 'matching_people': matching_people})

