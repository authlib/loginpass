"""
    loginpass.auth0
    ~~~~~~~~~~~~~~~

    Loginpass Backend of Auth0 (https://auth0.com) tenants'
    endpoints.

    :copyright: (c) 2018 by Hsiaoming Yang
    :license: BSD, see LICENSE for more details.
"""

from ._core import UserInfo, OAuthBackend, parse_id_token

ALLOW_REGIONS = ['us', 'eu', 'au']


def create_auth0_backend(name, tenant, region=None):
    """Create an Auth0 backend for one tenant."""

    if region and region not in ALLOW_REGIONS:
        raise ValueError('Not a vaild "region"')
    if not region or region == 'us':
        host = 'https://{}.auth0.com/'.format(tenant)
    else:
        host = 'https://{}.{}.auth0.com/'.format(tenant, region)

    authorize_url = '{}authorize'.format(host)
    token_url = '{}oauth/token'.format(host)

    class Auth0(OAuthBackend):
        OAUTH_TYPE = '2.0,oidc'
        OAUTH_NAME = name
        OAUTH_CONFIG = {
            'api_base_url': host,
            'access_token_url': token_url,
            'authorize_url': authorize_url,
            'client_kwargs': {'scope': 'openid email profile'},
        }
        JWK_SET_URL = '.well-known/jwks.json'.format(host)

        def profile(self, **kwargs):
            resp = self.get('userinfo', **kwargs)
            resp.raise_for_status()
            data = resp.json()
            return UserInfo(data)

        def parse_openid(self, token, nonce=None):
            return parse_id_token(
                self, token['id_token'],
                {"iss": {"values": [host]}},
                token.get('access_token'), nonce
            )

    return Auth0
