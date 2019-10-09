"""
    loginpass.hydra
    ~~~~~~~~~~~~~~~~

    Loginpass Backend of Ory Hydra (https://ory.sh) and its
    enterprise endpoints.

    Useful Links: https://www.ory.sh/docs/hydra/sdk/api

    - API documentation: https://www.ory.sh/docs/hydra/sdk/api

    :license: BSD, see LICENSE for more details.
"""

from ._core import UserInfo, OAuthBackend


def create_hydra_backend(name, hostname):
    """Build Hydra OAuth Backend."""
    api_base_url = 'https://{hostname}'.format(hostname=hostname)
    authorize_url = 'https://{hostname}/oauth2/auth'.format(hostname=hostname)
    token_url = 'https://{hostname}/oauth2/token'.format(hostname=hostname)

    class Hydra(OAuthBackend):
        OAUTH_TYPE = '2.0,oidc'
        OAUTH_NAME = name
        OAUTH_CONFIG = {
            'api_base_url': api_base_url,
            'access_token_url': token_url,
            'authorize_url': authorize_url
            # customisations can added in client kwargs
        }

        def profile(self, **kwargs):
            resp = self.get('userinfo', **kwargs)
            resp.raise_for_status()
            data = resp.json()
            if not kwargs.get('param_keys'):
                params = data
            else:
                params = {k: data[k] for k in kwargs.get('param_keys')}

            return UserInfo(params)

    return Hydra
