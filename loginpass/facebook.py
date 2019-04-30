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

from ._core import UserInfo, OAuthBackend, map_profile_fields


class Facebook(OAuthBackend):
    OAUTH_TYPE = '2.0'
    OAUTH_NAME = 'facebook'
    OAUTH_CONFIG = {
        'api_base_url': 'https://graph.facebook.com/v2.12',
        'access_token_url': 'https://graph.facebook.com/v2.12/oauth/access_token',
        'authorize_url': 'https://www.facebook.com/v2.12/dialog/oauth',
        'client_kwargs': {'scope': 'email public_profile'},
    }

    def profile(self, **kwargs):
        if 'params' not in kwargs:
            fields = [
                'id', 'name', 'first_name', 'middle_name', 'last_name',
                'email', 'website', 'gender', 'locale'
            ]
            kwargs['params'] = {'fields': ','.join(fields)}
        resp = self.get('me', **kwargs)
        resp.raise_for_status()
        return UserInfo(map_profile_fields(resp.json(), {
            'sub': lambda o: str(o['id']),
            'name': 'name',
            'given_name': 'first_name',
            'family_name': 'last_name',
            'middle_name': 'middle_name',
            'email': 'email',
            'website': 'website',
            'gender': 'gender',
            'locale': 'locale'
        }))
