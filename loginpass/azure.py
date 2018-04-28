"""
    loginpass.azure
    ~~~~~~~~~~~~~~~

    Loginpass Backend of Azure AD.

    :copyright: (c) 2018 by Hsiaoming Yang
    :license: AGPLv3+, see LICENSE for more details.
"""

from authlib.specs.oidc import UserInfo
from ._core import OAuthBackend, parse_id_token


def create_azure_backend(name, tenant):
    """Build Azure Active Directory OAuth Backend."""

    base_url = 'https://login.microsoftonline.com/'
    authorize_url = '{}{}/oauth2/authorize'.format(base_url, tenant)
    token_url = '{}{}/oauth2/token'.format(base_url, tenant)

    jwt_claims_options = {
        "iss": {
            "values": ['https://sts.windows.net/{}/'.format(tenant)]
        }
    }

    class AzureAD(OAuthBackend):
        OAUTH_TYPE = '2.0,oidc'
        OAUTH_NAME = name
        OAUTH_CONFIG = {
            'api_base_url': 'graph.microsoft.com',
            'access_token_url': token_url,
            'authorize_url': authorize_url,
            'client_kwargs': {'scope': 'openid email profile'},
        }
        JWK_SET_URL = '{}{}/discovery/keys'.format(base_url, tenant)

        def profile(self, **kwargs):
            url = '{}{}/openid/userinfo'.format(base_url, tenant)
            resp = self.get(url, **kwargs)
            resp.raise_for_status()
            return UserInfo(**resp.json())

        def parse_openid(self, token, nonce=None):
            return parse_id_token(
                self, token['id_token'], jwt_claims_options,
                token.get('access_token'), nonce
            )

    return AzureAD


Azure = create_azure_backend('azure', 'common')
