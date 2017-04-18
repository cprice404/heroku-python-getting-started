from django.shortcuts import render, redirect
from django.conf import settings
import json

from hello.utils.oauth import get_oauth_service, get_redirect_url
from hello.view_helpers.formset import handle_formset_request
from hello.view_helpers.tags import handle_tags_request,handle_replace_tag_request


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

    request.session['token'] = token
    return menu(request)

def menu(request):
    return render(request, 'menu.html',
                  context={'nation_slug': request.session['nation_slug']})

def tags(request):
    return handle_tags_request(request)

def formset(request):
    return handle_formset_request(request)

def replace_tag(request):
    return handle_replace_tag_request(request)