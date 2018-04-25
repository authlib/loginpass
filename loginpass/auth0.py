"""
    loginpass.auth0
    ~~~~~~~~~~~~~~~

    Loginpass Backend of Auth0 (https://auth0.com) tenants'
    endpoints.

    :copyright: (c) 2018 by Hsiaoming Yang
    :license: AGPLv3+, see LICENSE for more details.
"""

from authlib.specs.oidc import UserInfo
from ._core import OAuthBackend

ALLOW_REGIONS = ['us', 'eu', 'au']


def create_auth0_backend(name, tenant, region=None):
    """Create an Auth0 backend for one tenant."""

    if region and region not in ALLOW_REGIONS:
        raise ValueError('Not a vaild "region"')
    if not region or region == 'us':
        prefix = tenant
    else:
        prefix = '{}.{}'.format(tenant, region)
    api_base_url = 'https://{}.auth0.com'.format(prefix)
    authorize_url = 'https://{}.auth0.com/authorize'.format(prefix)
    token_url = 'https://{}.auth0.com/oauth/token'.format(prefix)

    class Auth0(OAuthBackend):
        OAUTH_TYPE = '2.0'
        OAUTH_NAME = name
        OAUTH_CONFIG = {
            'api_base_url': api_base_url,
            'access_token_url': token_url,
            'authorize_url': authorize_url,
            'client_kwargs': {'scope': 'openid profile'},
        }

        def profile(self):
            resp = self.get('userinfo')
            resp.raise_for_status()
            data = resp.json()
            return UserInfo(data)
    return Auth0
