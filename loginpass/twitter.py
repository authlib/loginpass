"""
    loginpass.twitter
    ~~~~~~~~~~~~~~~~~

    Loginpass Backend of Twitter (https://twitter.com).

    Useful Links:

    - Create App: https://apps.twitter.com/
    - API documentation: https://developer.twitter.com/

    :copyright: (c) 2018 by Hsiaoming Yang
    :license: BSD, see LICENSE for more details.
"""
from ._core import UserInfo, OAuthBackend


class Twitter(OAuthBackend):
    OAUTH_TYPE = '1.0'
    OAUTH_NAME = 'twitter'
    OAUTH_CONFIG = {
        'api_base_url': 'https://api.twitter.com/1.1/',
        'request_token_url': 'https://api.twitter.com/oauth/request_token',
        'access_token_url': 'https://api.twitter.com/oauth/access_token',
        'authorize_url': 'https://api.twitter.com/oauth/authenticate',
    }

    def profile(self, **kwargs):
        url = 'account/verify_credentials.json'
        if 'params' not in kwargs:
            kwargs['params'] = {
                'skip_status': True,
                'include_email': True
            }
        resp = self.get(url, **kwargs)
        resp.raise_for_status()
        data = resp.json()
        params = {
            'sub': data['id_str'],
            'name': data['name'],
            'email': data.get('email'),
            'locale': data.get('lang'),
            'picture': data.get('profile_image_url_https'),
            'preferred_username': data.get('screen_name'),
        }
        username = params['preferred_username']
        if username:
            params['profile'] = 'https://twitter.com/{}'.format(username)
        return UserInfo(params)
