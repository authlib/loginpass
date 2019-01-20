"""
    loginpass.azure
    ~~~~~~~~~~~~~~~

    Loginpass Backend of Azure AD.

    :copyright: (c) 2018 by Hsiaoming Yang
    :license: AGPLv3+, see LICENSE for more details.
"""

from ._core import UserInfo, OAuthBackend, parse_id_token

_BASE_URL = 'https://login.microsoftonline.com/'


def _create_azure_ad_class(name,
                           tenant,
                           authorize_url,
                           token_url,
                           jwt_claims_options):

    class AzureAD(OAuthBackend):
        OAUTH_TYPE = '2.0,oidc'
        OAUTH_NAME = name
        OAUTH_CONFIG = {
            'api_base_url': 'graph.microsoft.com',
            'access_token_url': token_url,
            'authorize_url': authorize_url,
            'client_kwargs': {'scope': 'openid email profile'},
        }
        JWK_SET_URL = '{}{}/discovery/keys'.format(_BASE_URL, tenant)

        def profile(self, **kwargs):
            url = '{}{}/openid/userinfo'.format(_BASE_URL, tenant)
            resp = self.get(url, **kwargs)
            resp.raise_for_status()
            return UserInfo(**resp.json())

        def parse_openid(self, token, nonce=None):
            return parse_id_token(
                self, token['id_token'], jwt_claims_options,
                token.get('access_token'), nonce
            )

    return AzureAD


def create_azurev1_backend(name, tenant):
    """Build Azure Active Directory OAuth Backend."""

    authorize_url = '{}{}/oauth2/authorize'.format(_BASE_URL, tenant)
    token_url = '{}{}/oauth2/token'.format(_BASE_URL, tenant)

    jwt_claims_options = {
        "iss": {
            "values": ['https://sts.windows.net/{}/'.format(tenant)]
        }
    }

    return _create_azure_ad_class(name,
                                  tenant,
                                  authorize_url,
                                  token_url,
                                  jwt_claims_options)


def create_azurev2_backend(name, tenant):
    """Build Azure Active Directory V2 OAuth Backend."""

    authorize_url = '{}{}/oauth2/v2.0/authorize'.format(_BASE_URL, tenant)
    token_url = '{}{}/oauth2/v2.0/token'.format(_BASE_URL, tenant)

    jwt_claims_options = {
        "iss": {
            "values": ['{}{}/v2.0'.format(_BASE_URL, tenant)]
        }
    }

    return _create_azure_ad_class(name,
                                  tenant,
                                  authorize_url,
                                  token_url,
                                  jwt_claims_options)


create_azure_backend = create_azurev1_backend
Azure = create_azure_backend('azure', 'common')
