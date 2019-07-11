"""
    loginpass.azure
    ~~~~~~~~~~~~~~~

    Loginpass Backend of Azure AD.

    :copyright: (c) 2018 by Hsiaoming Yang
    :license: BSD, see LICENSE for more details.
"""

from ._core import UserInfo, OAuthBackend, parse_id_token

_BASE_URL = 'https://login.microsoftonline.com/'


def create_azure_backend(name, tenant, version=1, claims_options=None):
    if version == 1:
        authorize_url = '{}{}/oauth2/authorize'.format(_BASE_URL, tenant)
        token_url = '{}{}/oauth2/token'.format(_BASE_URL, tenant)
        issuer_url = 'https://sts.windows.net/{}/'.format(tenant)
        if claims_options is None:
            claims_options = {
                'iss': {
                    'values': [issuer_url]
                }
            }

    elif version == 2:
        authorize_url = '{}{}/oauth2/v2.0/authorize'.format(_BASE_URL, tenant)
        token_url = '{}{}/oauth2/v2.0/token'.format(_BASE_URL, tenant)
        issuer_url = '{}{}/v2.0'.format(_BASE_URL, tenant)

        if claims_options is None:

            def validate_iss(claims, value):
                iss = 'https://login.microsoftonline.com/{}/v2.0'.format(claims['tid'])
                return iss == value

            claims_options = {
                'iss': {
                    'essential': True,
                    'validate': validate_iss,
                }
            }

    else:
        raise ValueError('Invalid version')

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
                self, token['id_token'], claims_options,
                token.get('access_token'), nonce
            )

    class AzureADv2(AzureAD):
        JWK_SET_URL = '{}{}/discovery/v2.0/keys'.format(_BASE_URL, tenant)

        def profile(self, **kwargs):
            return self.parse_openid(**kwargs)

    if version == 2:
        return AzureADv2
    else:
        return AzureAD


Azure = create_azure_backend('azure', 'common')
