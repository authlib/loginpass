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

from ._core import UserInfo, OAuthBackend, map_profile_fields
from ._consts import version, homepage


# see: https://github.com/reddit-archive/reddit/wiki/API#rules
UA = 'web:loginpass:{} (by /u/lepture) (+{})'.format(version, homepage)


class Reddit(OAuthBackend):
    OAUTH_TYPE = '2.0'
    OAUTH_NAME = 'reddit'
    OAUTH_CONFIG = {
        'api_base_url': 'https://oauth.reddit.com/api/v1/',
        'access_token_url': 'https://www.reddit.com/api/v1/access_token',
        'authorize_url': 'https://www.reddit.com/api/v1/authorize',
        'client_kwargs': {'scope': 'identity'},
    }

    DEFAULT_USER_AGENT = UA

    def profile(self, **kwargs):
        resp = self.get('me', **kwargs)
        resp.raise_for_status()
        return UserInfo(map_profile_fields(resp.json(), {
            'sub': 'id',
            'name': 'name',
            'email': 'email',
            'preferred_username': 'name',
            'profile': _get_profile,
            'picture': 'icon_img',
            'email_verified': 'has_verified_email',
        }))


def _get_profile(data):
    return 'https://www.reddit.com/user/{}/'.format(data['name'])
