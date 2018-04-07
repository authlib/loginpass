class OAuthBackend(object):
    """Backend for OAuth Registry"""
    OAUTH_TYPE = None
    OAUTH_NAME = None
    OAUTH_CONFIG = None
    JWK_SET_URL = None

    @classmethod
    def register_to(cls, oauth):
        client_mixin = _get_oauth_client_cls(oauth)
        config = cls.OAUTH_CONFIG.copy()
        if client_mixin:
            class RemoteApp(cls, client_mixin):
                pass
            config['client_cls'] = RemoteApp
        return oauth.register(cls.OAUTH_NAME, **config)

    def fetch_jwk_set(self, force=False):
        if not self.JWK_SET_URL:
            return None

        jwk_set = getattr(self, '_jwk_set', None)
        if jwk_set and not force:
            return jwk_set

        resp = self.get(self.JWK_SET_URL, withhold_token=True)
        self._jwk_set = resp.json()
        return self._jwk_set


def register_to(registry, backend_cls):
    return backend_cls.register_to(registry)


def _get_oauth_client_cls(oauth):
    from authlib.flask.client import (
        OAuth as FlaskOAuth,
        RemoteApp as FlaskRemoteApp,
    )
    from authlib.django.client import (
        OAuth as DjangoOAuth,
        RemoteApp as DjangoRemoteApp,
    )

    if isinstance(oauth, FlaskOAuth):
        return FlaskRemoteApp

    if isinstance(oauth, DjangoOAuth):
        return DjangoRemoteApp
