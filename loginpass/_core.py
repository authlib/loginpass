from authlib.client import OAuthClient
from authlib.jose import jwt, jwk
from authlib.oidc.core import CodeIDToken, ImplicitIDToken, UserInfo


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


def map_profile_fields(data, fields):
    """Copy profile data from site-specific to standard field names.
    Standard keys will only be set if the site data for that key is not
    ``None`` and not empty string.

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

        if value is not None and value != '':
            profile[dst] = value

    return profile


def parse_id_token(remote, id_token, claims_options,
                   access_token=None, nonce=None):
    """Parse UserInfo from id_token."""

    def load_key(header, payload):
        jwk_set = remote.fetch_jwk_set()
        try:
            return jwk.loads(jwk_set, header.get('kid'))
        except ValueError:
            jwk_set = remote.fetch_jwk_set(force=True)
            return jwk.loads(jwk_set, header.get('kid'))

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
        id_token, key=load_key,
        claims_cls=claims_cls,
        claims_options=claims_options,
        claims_params=claims_params,
    )
    claims.validate(leeway=120)
    return UserInfo(claims)
