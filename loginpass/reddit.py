"""
    loginpass.reddit
    ~~~~~~~~~~~~~~~~

    Loginpass Backend of Reddit (https://www.reddit.com).

    Useful Links:

    - Create App: https://www.reddit.com/prefs/apps
    - API documentation: http://www.reddit.com/dev/api
"""

from authlib.specs.oidc import UserInfo
from ._core import OAuthBackend


class Reddit(OAuthBackend):
    OAUTH_TYPE = '2.0'
    OAUTH_NAME = 'reddit'
    OAUTH_CONFIG = {
        'api_base_url': 'https://oauth.reddit.com/api/v1/',
        'access_token_url': 'https://www.reddit.com/api/v1/access_token',
        'authorize_url': 'https://www.reddit.com/api/v1/authorize',
        'client_kwargs': {'scope': 'identity'},
    }

    def profile(self):
        resp = self.get('me')
        # TODO
        params = resp.json()
        return UserInfo(params)
