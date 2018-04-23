"""
    loginpass.reddit
    ~~~~~~~~~~~~~~~~

    Loginpass Backend of Reddit (https://www.reddit.com).

    Useful Links:

    - Create App: https://www.reddit.com/prefs/apps
    - API documentation: http://www.reddit.com/dev/api

    :copyright: (c) 2018 by Hsiaoming Yang
    :license: AGPLv3+, see LICENSE for more details.
"""

from authlib.specs.oidc import UserInfo
from ._core import OAuthBackend
from ._version import version, homepage


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

    def profile(self):
        resp = self.get('me')
        data = resp.json()
        profile = 'https://www.reddit.com/user/{}/'.format(data['name'])
        params = {
            'sub': data['id'],
            'name': data['name'],
            'email': data.get('email'),
            'preferred_username': data['name'],
            'profile': profile,
            'picture': data['icon_img'],
            'email_verified': data['has_verified_email'],
        }
        return UserInfo(params)
