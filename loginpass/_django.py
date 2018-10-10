from authlib.common.security import generate_token
from ._core import register_to


def create_django_urlpatterns(backend, oauth, handle_authorize):
    from django.urls import path
    from authlib.django.client import RemoteApp

    remote = register_to(backend, oauth, RemoteApp)
    nonce_key = '_{}:nonce'.format(backend.OAUTH_NAME)
    auth_route_name = 'loginpass_{}_auth'.format(backend.OAUTH_NAME)
    login_route_name = 'loginpass_{}_login'.format(backend.OAUTH_NAME)

    auth = create_auth_endpoint(remote, nonce_key, handle_authorize)
    login = create_login_endpoint(remote, backend, nonce_key, auth_route_name)

    return [
        path('auth/', auth, name=auth_route_name),
        path('login/', login, name=login_route_name),
    ]


def create_auth_endpoint(remote, nonce_key, handle_authorize):

    def auth(request):
        id_token = request.GET.get('id_token')
        if request.GET.get('code'):
            token = remote.authorize_access_token(request)
            if id_token:
                token['id_token'] = id_token
        elif id_token:
            token = {'id_token': id_token}
        elif request.GET.get('oauth_verifier'):
            # OAuth 1
            token = remote.authorize_access_token(request)
        else:
            # handle failed
            return handle_authorize(remote, None, None)
        if 'id_token' in token:
            nonce = request.session[nonce_key]
            user_info = remote.parse_openid(token, nonce)
        else:
            user_info = remote.profile(token=token)
        return handle_authorize(request, remote, token, user_info)
    return auth


def create_login_endpoint(remote, backend, nonce_key, auth_route_name):
    from django.conf import settings
    from django.urls import reverse

    config = getattr(settings, 'AUTHLIB_OAUTH_CLIENTS', None)
    authorize_params = None
    if config:
        backend_config = config.get(backend.OAUTH_NAME)
        if backend_config:
            authorize_params = backend_config.get('authorize_params')

    def login(request):
        redirect_uri = request.build_absolute_uri(reverse(auth_route_name))
        params = {}
        if authorize_params:
            params.udpate(authorize_params)
        if 'oidc' in backend.OAUTH_TYPE:
            nonce = generate_token(20)
            request.session[nonce_key] = nonce
            params['nonce'] = nonce
        return remote.authorize_redirect(request, redirect_uri, **params)
    return login
