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


class ORCiD(object):
    NAME = 'orcid'
    OAUTH_CONFIG = {
        'api_base_url': 'https://orcid.org/',
        'server_metadata_url': 'https://orcid.org/.well-known/openid-configuration',
        'client_kwargs': {'scope': 'openid email profile'},
    }
