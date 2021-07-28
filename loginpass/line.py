"""
    loginpass.line
    ~~~~~~~~~~~~~~~~~~
    Loginpass Backend of LINE (line.me)
    Useful Links:
    - Dev Portal: https://developers.line.biz/
    :copyright: (c) 2021 by Jakee Indapanya
    :license: BSD, see LICENSE for more details.
"""

from ._core import map_profile_fields


def normalize_userinfo(client, data):
    return map_profile_fields(data, {
        'sub': 'userId',
        'username': 'displayName',
        'status': 'statusMessage',
        'picture': 'pictureUrl'
    })


class LINE(object):
    NAME = 'line'
    OAUTH_CONFIG = {
        'api_base_url': 'https://access.line.me/v2',
        'access_token_url': 'https://api.line.me/oauth2/v2.1/token',
        'authorize_url': 'https://access.line.me/oauth2/v2.1/authorize',
        'userinfo_endpoint': 'https://api.line.me/v2/profile',
        'client_kwargs': {'scope': 'profile'},
        'userinfo_compliance_fix': normalize_userinfo,
    }
