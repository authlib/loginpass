"""
    loginpass.auth0
    ~~~~~~~~~~~~~~~

    Loginpass Backend of Auth0 (https://auth0.com) tenants'
    endpoints.

    :copyright: (c) 2018 by Hsiaoming Yang
    :license: BSD, see LICENSE for more details.
"""

ALLOW_REGIONS = ['us', 'eu', 'au']


def create_auth0_backend(name, tenant, region=None):
    """Create an Auth0 backend for one tenant."""

    if region and region not in ALLOW_REGIONS:
        raise ValueError('Not a vaild "region"')
    if not region or region == 'us':
        host = 'https://{}.auth0.com/'.format(tenant)
    else:
        host = 'https://{}.{}.auth0.com/'.format(tenant, region)

    class Auth0(object):
        NAME = name
        OAUTH_CONFIG = {
            'api_base_url': host,
            'server_metadata_url': host + '.well-known/openid-configuration',
            'client_kwargs': {'scope': 'openid email profile'},
        }

    return Auth0
