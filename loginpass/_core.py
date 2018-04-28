from authlib.client import OAuthClient
from authlib.common.security import generate_token
from authlib.specs.rfc7519 import jwt
from authlib.specs.oidc import CodeIDToken, ImplicitIDToken, UserInfo


class OAuthBackend(OAuthClient):
    """Backend for OAuth Registry"""
    OAUTH_TYPE = None
    OAUTH_NAME = None
    OAUTH_CONFIG = None
    JWK_SET_URL = None

    def fetch_jwk_set(self, force=False):
        if not self.JWK_SET_URL:
            return None

        jwk_set = getattr(self, '_jwk_set', None)
        if jwk_set and not force:
            return jwk_set

        resp = self.get(self.JWK_SET_URL, withhold_token=True)
        self._jwk_set = resp.json()
        return self._jwk_set


def _get_oauth_client_cls(oauth):
    try:
        from authlib.flask.client import (
            OAuth as FlaskOAuth,
            RemoteApp as FlaskRemoteApp,
        )
        if isinstance(oauth, FlaskOAuth):
            return FlaskRemoteApp
    except ImportError:
        try:
            from authlib.django.client import (
                OAuth as DjangoOAuth,
                RemoteApp as DjangoRemoteApp,
            )
            if isinstance(oauth, DjangoOAuth):
                return DjangoRemoteApp
        except ImportError:
            pass


def register_to(backend, oauth, client_base=None):
    """Register a backend to OAuth instance.

    :param backend: An OAuthBackend
    :param oauth: Authlib OAuth instance
    :param client_base: This function will find a client_base
        automatically, Flask or Django.
    :return: backend instance
    """
    if client_base is None:
        client_base = _get_oauth_client_cls(oauth)

    config = backend.OAUTH_CONFIG.copy()
    if client_base:
        class RemoteApp(client_base, backend):
            pass
        config['client_cls'] = RemoteApp
    return oauth.register(backend.OAUTH_NAME, overwrite=True, **config)


def create_flask_blueprint(backend, oauth, handle_authorize):
    """Create a Flask blueprint that you can register it directly to Flask
    app. The blueprint contains two route: ``/auth`` and ``/login``::

        from flask import Flask
        from authlib.flask.client import OAuth
        from loginpass import create_flask_blueprint, GitHub

        app = Flask(__name__)
        oauth = OAuth(app)


        def handle_authorize(remote, token, user_info):
            if token:
                save_token(remote.name, token)
            if user_info:
                save_user(user_info)
                return user_page
            raise some_error

        github_bp = create_flask_blueprint(GitHub, oauth, handle_authorize)
        app.register_blueprint(github_bp, url_prefix='/github')

        # visit /github/login
        # callback /github/auth

    :param backend: An OAuthBackend
    :param oauth: Authlib Flask OAuth instance
    :param handle_authorize: A function to handle authorized response
    :return: Flask Blueprint instance
    """
    from flask import Blueprint, request, url_for, current_app, session
    from authlib.flask.client import RemoteApp

    remote = register_to(backend, oauth, RemoteApp)
    nonce_key = '_{}:nonce'.format(backend.OAUTH_NAME)
    bp = Blueprint('loginpass_' + backend.OAUTH_NAME, __name__)

    @bp.route('/auth')
    def auth():
        id_token = request.args.get('id_token')
        if request.args.get('code'):
            token = remote.authorize_access_token()
            if id_token:
                token['id_token'] = id_token
        elif id_token:
            token = {'id_token': id_token}
        else:
            # handle failed
            return handle_authorize(remote, None, None)
        if 'id_token' in token:
            nonce = session[nonce_key]
            user_info = remote.parse_openid(token, nonce)
        else:
            user_info = remote.profile()
        return handle_authorize(remote, token, user_info)

    @bp.route('/login')
    def login():
        redirect_uri = url_for('.auth', _external=True)
        conf_key = '{}_AUTHORIZE_PARAMS'.format(backend.OAUTH_NAME.upper())
        params = current_app.config.get(conf_key, {})
        if 'oidc' in backend.OAUTH_TYPE:
            nonce = generate_token(20)
            session[nonce_key] = nonce
            params['nonce'] = nonce
        return remote.authorize_redirect(redirect_uri, **params)

    return bp


def create_django_urlpatterns(backend, oauth, handle_authorize):
    from django.conf import settings
    from django.urls import path, reverse
    from authlib.django.client import RemoteApp

    config = getattr(settings, 'AUTHLIB_OAUTH_CLIENTS', None)
    authorize_params = None
    if config:
        backend_config = config.get(backend.OAUTH_NAME)
        if backend_config:
            authorize_params = backend_config.get('authorize_params')

    remote = register_to(backend, oauth, RemoteApp)
    nonce_key = '_{}:nonce'.format(backend.OAUTH_NAME)
    auth_route_name = 'loginpass_{}_auth'.format(backend.OAUTH_NAME)
    login_route_name = 'loginpass_{}_login'.format(backend.OAUTH_NAME)

    def auth(request):
        id_token = request.GET.get('id_token')
        if request.GET.get('code'):
            token = remote.authorize_access_token(request)
            if id_token:
                token['id_token'] = id_token
        elif id_token:
            token = {'id_token': id_token}
        else:
            # handle failed
            return handle_authorize(remote, None, None)
        if 'id_token' in token:
            nonce = request.session[nonce_key]
            user_info = remote.parse_openid(token, nonce)
        else:
            user_info = remote.profile(token=token)
        return handle_authorize(request, remote, token, user_info)

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

    return [
        path('auth/', auth, name=auth_route_name),
        path('login/', login, name=login_route_name),
    ]


def map_profile_fields(data, fields):
    """Copy profile data from site-specific to standard field names.
    Standard keys will only be set if the site data for that key is not
    ``None``.

    :param data: Profile data from the site, to be modified in place.
    :param fields: Map of ``{destination: source}``. Destination is the
        standard name. Source source is the site-specific name, or
        a callable taking ``data`` and returning the value.
    :return: UserInfo fields
    """
    profile = {}
    for dst, src in fields.items():
        if callable(src):
            value = src(data)
        else:
            value = data.get(src)

        if value is not None:
            profile[dst] = value

    return profile


def parse_id_token(remote, id_token, claims_options,
                   access_token=None, nonce=None):
    """Parse UserInfo from id_token."""
    jwk_set = remote.fetch_jwk_set()
    claims_params = dict(
        nonce=nonce,
        client_id=remote.client_id,
    )
    if access_token:
        claims_params['access_token'] = access_token
        claims_cls = CodeIDToken
    else:
        claims_cls = ImplicitIDToken
    claims = jwt.decode(
        id_token, key=jwk_set,
        claims_cls=claims_cls,
        claims_options=claims_options,
        claims_params=claims_params,
    )
    claims.validate(leeway=120)
    return UserInfo(claims)
