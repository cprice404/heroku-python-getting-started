import urllib

from django.shortcuts import render
from hello.utils.oauth import get_oauth_service


def handle_tags_request(request):
    tag_prefix = None
    selected_tag = None
    edit_person_id = None
    if request.method == 'POST':
        tag_prefix = request.POST.get('tag_prefix')
        selected_tag = request.POST.get('selected_tag')
        edit_person_id = request.POST.get('edit_person_id')
        save_person(edit_person_id, request)
        edit_person_id = None
    elif request.method == 'GET':
        tag_prefix = request.GET.get('tag_prefix')
        selected_tag = request.GET.get('selected_tag')
        edit_person_id = request.GET.get('edit_person_id')

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
    selected_tag_map = None
    if selected_tag:
        url = "https://" + nation_slug + \
              ".nationbuilder.com/api/v1/tags/" + \
              selected_tag + \
              "/people?limit=1000"
        people_response = session.get(url,
                                      params={'format': 'json'},
                                      headers={'content-type': 'application/json'})
        people = people_response.json()['results']
        for person in people:
            # print "PERSON KEYS: '%s'" % person.keys()
            # print "PERSON TAGS: '%s'" % person['tags']
            # print "PERSON ID: '%s'" % person['id']
            # print "PERSON: '%s'" % person
            team_tags = filter(lambda t: t.lower().startswith("team"),
                               person['tags'])
            person_map = {'id': str(person['id']),
                          'first_name': person['first_name'],
                          'last_name': person['last_name'],
                          'team_tags': team_tags,
                          'email': person['email'],
                          'phone': person['phone'],
                          'address': person['primary_address']}
            matching_people.append(person_map)
            # print("EDIT_PERSON_ID: '%s'" % edit_person_id)
        selected_tag_map = {'raw': selected_tag,
                            'encoded': urllib.quote_plus(selected_tag)}

    return render(request, 'tags.html', context={'tags': tags,
                                                 'tag_prefix': tag_prefix or '',
                                                 'filtered_tags': filtered_tags,
                                                 'selected_tag': selected_tag_map,
                                                 'edit_person_id': edit_person_id,
                                                 'matching_people': matching_people})

def save_person(person_id, request):
    print("SAVING PERSON: '%s'" % request.POST)
    pass