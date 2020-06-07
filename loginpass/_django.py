
def create_django_urlpatterns(backend, oauth, handle_authorize):
    from authlib.integrations.django_client import DjangoRemoteApp
    from django.urls import path

    class RemoteApp(backend, DjangoRemoteApp):
        OAUTH_APP_CONFIG = backend.OAUTH_CONFIG

    token_name = '_loginpass_{}_token'.format(backend.NAME)
    auth_route_name = 'loginpass_{}_auth'.format(backend.NAME)
    login_route_name = 'loginpass_{}_login'.format(backend.NAME)

    remote = oauth.register(
        backend.NAME,
        overwrite=True,
        fetch_token=lambda request: getattr(request, token_name, None),
        client_cls=RemoteApp,
    )

    auth = create_auth_endpoint(remote, handle_authorize)
    login = create_login_endpoint(remote, backend, auth_route_name)

    return [
        path('auth/', auth, name=auth_route_name),
        path('login/', login, name=login_route_name),
    ]


def create_auth_endpoint(remote, handle_authorize):

    def auth(request):
        from django.http import HttpResponse

        if request.method not in ('GET', 'POST'):
            return HttpResponse(status=405)

        method = getattr(request, request.method)

        id_token = method.get('id_token')
        if method.get('code'):
            token = remote.authorize_access_token(request)
            if id_token:
                token['id_token'] = id_token
        elif id_token:
            token = {'id_token': id_token}
        elif method.get('oauth_verifier'):
            # OAuth 1
            token = remote.authorize_access_token(request)
        else:
            # handle failed
            return handle_authorize(remote, None, None)
        if 'id_token' in token:
            user_info = remote.parse_id_token(request, token)
        else:
            token_name = '_loginpass_{}_token'.format(remote.name)
            setattr(request, token_name, token)
            user_info = remote.userinfo(request=request, token=token)
        return handle_authorize(request, remote, token, user_info)
    return auth


def create_login_endpoint(remote, backend, auth_route_name):
    from django.conf import settings
    from django.urls import reverse

    config = getattr(settings, 'AUTHLIB_OAUTH_CLIENTS', None)
    authorize_params = None
    if config:
        backend_config = config.get(backend.NAME)
        if backend_config:
            authorize_params = backend_config.get('authorize_params')

    def login(request):
        redirect_uri = request.build_absolute_uri(reverse(auth_route_name))
        params = {}
        if authorize_params:
            params.udpate(authorize_params)
        return remote.authorize_redirect(request, redirect_uri, **params)
    return login
