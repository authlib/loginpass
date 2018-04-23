"""
    loginpass.google
    ~~~~~~~~~~~~~~~~

    This module contains a loginpass backend of Google,
    and a ServiceAccount requests Session.

    :copyright: (c) 2018 by Hsiaoming Yang
    :license: AGPLv3+, see LICENSE for more details.
"""

import json
from authlib.client import AssertionSession
from authlib.specs.rfc7519 import JWT
from authlib.specs.oidc import CodeIDToken, UserInfo
from ._core import OAuthBackend


GOOGLE_API_URL = 'https://www.googleapis.com/'
GOOGLE_TOKEN_URL = GOOGLE_API_URL + 'oauth2/v4/token'
GOOGLE_JWK_URL = GOOGLE_API_URL + 'oauth2/v3/certs'
GOOGLE_AUTH_URL = (
    'https://accounts.google.com/o/oauth2/v2/auth'
    '?access_type=offline'
)
GOOGLE_CLAIMS_OPTIONS = {
    "iss": {
        "values": ['https://accounts.google.com', 'accounts.google.com']
    }
}


class Google(OAuthBackend):
    OAUTH_TYPE = '2.0,oidc'
    OAUTH_NAME = 'google'
    OAUTH_CONFIG = {
        'api_base_url': GOOGLE_API_URL,
        'access_token_url': GOOGLE_TOKEN_URL,
        'authorize_url': GOOGLE_AUTH_URL,
        'client_kwargs': {'scope': 'openid email profile'},
    }
    JWK_SET_URL = GOOGLE_JWK_URL

    def profile(self):
        resp = self.get('oauth2/v3/userinfo')
        resp.raise_for_status()
        return UserInfo(**resp.json())

    def parse_openid(self, token, nonce=None):
        jwk_set = self.fetch_jwk_set()
        id_token = token['id_token']
        claims_params = dict(
            nonce=nonce,
            client_id=self.client_id,
            access_token=token['access_token']
        )
        jwt = JWT()
        claims = jwt.decode(
            id_token, key=jwk_set,
            claims_cls=CodeIDToken,
            claims_options=GOOGLE_CLAIMS_OPTIONS,
            claims_params=claims_params,
        )
        claims.validate(leeway=120)
        return UserInfo(claims)


class GoogleServiceAccount(AssertionSession):
    @classmethod
    def from_service_account_file(cls, conf_file, scope, subject=None):
        with open(conf_file, 'r') as f:
            conf = json.load(f)

        token_url = conf['token_uri']
        issuer = conf['client_email']
        key = conf['private_key']
        key_id = conf.get('private_key_id')

        header = {'alg': 'RS256'}
        if key_id:
            header['kid'] = key_id

        # Google puts scope in payload
        claims = {'scope': scope}
        return cls(
            grant_type=cls.JWT_BEARER_GRANT_TYPE,
            token_url=token_url,
            issuer=issuer,
            audience=token_url,
            claims=claims,
            subject=subject,
            key=key,
            header=header,
        )
