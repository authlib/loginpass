"""
    loginpass.box
    ~~~~~~~~~~~~~~~~~

    Loginpass Backend of Box (https://box.com).

    Useful Links:

    - Create App: https://account.box.com/developers/services
    - API documentation: https://developer.box.com/reference

    :copyright: (c) 2019 by Isaac J. Galvan
    :license: BSD, see LICENSE for more details.
"""

from authlib.common.urls import url_decode
from ._core import UserInfo, OAuthBackend

class Box(OAuthBackend):
    OAUTH_TYPE = '2.0'
    OAUTH_NAME = 'box'
    OAUTH_CONFIG = {
        'api_base_url': 'https://api.box.com/2.0/',
        'access_token_url': 'https://api.box.com/oauth2/token',
        'authorize_url': 'https://account.box.com/api/oauth2/authorize',
        'client_kwargs': {
            'token_endpoint_auth_method': 'client_secret_post'
        }
    }

    def profile(self, **kwargs):
        resp = self.get('users/me', **kwargs)
        resp.raise_for_status()
        data = resp.json()
        params = {
            'sub': data['id'],
            'name': data['name'],
            'email': data['login'],
            'picture': data['avatar_url']

        }
        return UserInfo(params)
