from django.conf import settings
from rauth import OAuth2Service

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