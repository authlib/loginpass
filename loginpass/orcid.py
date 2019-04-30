"""
st
    loginpass.orcid
    ~~~~~~~~~~~~~~~

    Loginpass Backend of ORCiD (https://orcid.org).

    Useful Links:

    - Endpoint signup: https://orcid.org/developer-tools

    :copyright: (c) 2019 by Bryan Newbold
    :license: BSD, see LICENSE for more details.
"""

from ._core import UserInfo, OAuthBackend, parse_id_token


_host = 'https://orcid.org'
_authorize_url = '{}/oauth/authorize'.format(_host)
_token_url = '{}/oauth/token'.format(_host)

class ORCiD(OAuthBackend):
    OAUTH_TYPE = '2.0,oidc'
    OAUTH_NAME = 'orcid'
    OAUTH_CONFIG = {
        'api_base_url': _host,
        'access_token_url': _token_url,
        'authorize_url': _authorize_url,
        'client_kwargs': {'scope': 'openid email profile'},
    }
    JWK_SET_URL = '{}/oauth/jwks'.format(_host)

    def profile(self, **kwargs):
        resp = self.get('userinfo', **kwargs)
        resp.raise_for_status()
        data = resp.json()
        data['orcid'] = data['sub']
        return UserInfo(data)

    def parse_openid(self, token, nonce=None):
        return parse_id_token(
            self, token['id_token'],
            {"iss": {"values": [_host]}},
            token.get('access_token'), nonce
        )

