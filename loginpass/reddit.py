"""
    loginpass.reddit
    ~~~~~~~~~~~~~~~~

    Loginpass Backend of Reddit (https://www.reddit.com).

    Useful Links:

    - Create App: https://www.reddit.com/prefs/apps
    - API documentation: http://www.reddit.com/dev/api

    :copyright: (c) 2018 by Hsiaoming Yang
    :license: BSD, see LICENSE for more details.
"""

from ._core import map_profile_fields
from ._consts import version, homepage


# see: https://github.com/reddit-archive/reddit/wiki/API#rules
UA = 'web:loginpass:{} (by /u/lepture) (+{})'.format(version, homepage)


def normalize_userinfo(client, data):
    return map_profile_fields(data, {
        'sub': 'id',
        'name': 'name',
        'email': 'email',
        'preferred_username': 'name',
        'profile': _get_profile,
        'picture': 'icon_img',
        'email_verified': 'has_verified_email',
    })


class Reddit(object):
    NAME = 'reddit'
    OAUTH_CONFIG = {
        'api_base_url': 'https://oauth.reddit.com/api/v1/',
        'access_token_url': 'https://www.reddit.com/api/v1/access_token',
        'authorize_url': 'https://www.reddit.com/api/v1/authorize',
        'client_kwargs': {'scope': 'identity'},
        'userinfo_endpoint': 'me',
        'userinfo_compliance_fix': normalize_userinfo,
    }
    DEFAULT_USER_AGENT = UA


def _get_profile(data):
    return 'https://www.reddit.com/user/{}/'.format(data['name'])
