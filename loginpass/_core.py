from authlib.client import OAuthClient


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
    if client_base is None:
        client_base = _get_oauth_client_cls(oauth)

    config = backend.OAUTH_CONFIG.copy()
    if client_base:
        class RemoteApp(client_base, backend):
            pass
        config['client_cls'] = RemoteApp
    return oauth.register(backend.OAUTH_NAME, overwrite=True, **config)


def create_flask_blueprint(backend, oauth, handle_authorize):
    from flask import Blueprint, url_for, current_app
    from authlib.flask.client import RemoteApp

    remote = register_to(backend, oauth, RemoteApp)
    bp = Blueprint('loginpass_' + backend.OAUTH_NAME, __name__)

    @bp.route('/auth')
    def auth():
        token = remote.authorize_access_token()
        print(token)
        if 'id_token' in token:
            user_info = remote.parse_openid(token)
        else:
            user_info = remote.profile()
        return handle_authorize(remote, token, user_info)

    @bp.route('/login')
    def login():
        redirect_uri = url_for('.auth', _external=True)
        conf_key = '{}_AUTHORIZE_PARAMS'.format(backend.OAUTH_NAME.upper())
        params = current_app.config.get(conf_key, {})
        return remote.authorize_redirect(redirect_uri, **params)

    return bp


def map_profile_fields(data, fields):
    """Copy profile data from site-specific to standard field names.
    Standard keys will only be set if the site data for that key is not
    ``None``.

    :param data: Profile data from the site, to be modified in place.
    :param fields: Map of ``{destination: source}``. Destination is the
        standard name. Source source is the site-specific name, or
        a callable taking ``data`` and returning the value.
    :return: The same ``data`` dict passed in, with new keys set.
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
