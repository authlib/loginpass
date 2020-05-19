"""
    loginpass.facebook
    ~~~~~~~~~~~~~~~~~~

    Loginpass Backend of Facebook (https://facebook.com).

    Useful Links:

    - Create App: https://developers.facebook.com/apps
    - API documentation: https://developers.facebook.com/docs/graph-api

    :copyright: (c) 2018 by Hsiaoming Yang
    :license: BSD, see LICENSE for more details.
"""

from ._core import map_profile_fields


USERINFO_FIELDS = [
    'id', 'name', 'first_name', 'middle_name', 'last_name',
    'email', 'website', 'gender', 'locale'
]
USERINFO_ENDPOINT = 'me?fields=' + ','.join(USERINFO_FIELDS)


def normalize_userinfo(client, data):
    return map_profile_fields(data, {
        'sub': lambda o: str(o['id']),
        'name': 'name',
        'given_name': 'first_name',
        'family_name': 'last_name',
        'middle_name': 'middle_name',
        'email': 'email',
        'website': 'website',
        'gender': 'gender',
        'locale': 'locale'
    })


class Facebook(object):
    NAME = 'facebook'
    OAUTH_CONFIG = {
        'api_base_url': 'https://graph.facebook.com/v7.0/',
        'access_token_url': 'https://graph.facebook.com/v7.0/oauth/access_token',
        'authorize_url': 'https://www.facebook.com/v7.0/dialog/oauth',
        'client_kwargs': {'scope': 'email public_profile'},
        'userinfo_endpoint': USERINFO_ENDPOINT,
        'userinfo_compliance_fix': normalize_userinfo,
    }
