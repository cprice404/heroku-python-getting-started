from django.shortcuts import render
from hello.utils.oauth import get_oauth_service


def handle_tags_request(request):
    tag_prefix = request.POST.get('tag_prefix')

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
        filtered_tags = filter(lambda x: x.lower().startswith(tag_prefix.lower()),
                               tags)

    matching_people = []
    filtered_tag_index = 0
    while (len(matching_people) < 10) and (filtered_tag_index < len(filtered_tags)):
        url = "https://" + nation_slug + \
              ".nationbuilder.com/api/v1/tags/" + \
              filtered_tags[filtered_tag_index] + \
              "/people"
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

