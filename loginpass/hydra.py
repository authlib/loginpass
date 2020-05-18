"""
    loginpass.hydra
    ~~~~~~~~~~~~~~~~

    Loginpass Backend of Ory Hydra (https://ory.sh) and its
    enterprise endpoints.

    Useful Links: https://www.ory.sh/docs/hydra/sdk/api

    - API documentation: https://www.ory.sh/docs/hydra/sdk/api

    :license: BSD, see LICENSE for more details.
"""


def create_hydra_backend(name, hostname):
    """Build Hydra OAuth Backend."""
    api_base_url = 'https://{}'.format(hostname)
    authorize_url = 'https://{}/oauth2/auth'.format(hostname)
    token_url = 'https://{}/oauth2/token'.format(hostname)

    class Hydra(object):
        NAME = name
        OAUTH_CONFIG = {
            'api_base_url': api_base_url,
            'access_token_url': token_url,
            'authorize_url': authorize_url,
            'userinfo_endpoint': 'userinfo',
            # customisations can added in client kwargs
        }

    return Hydra
