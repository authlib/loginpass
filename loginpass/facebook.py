"""
    loginpass.facebook
    ~~~~~~~~~~~~~~~~~~

    Loginpass Backend of Facebook (https://facebook.com).

    Useful Links:

    - Create App: https://developers.facebook.com/apps
    - API documentation: https://developers.facebook.com/docs/graph-api

    :copyright: (c) 2018 by Hsiaoming Yang
    :license: AGPLv3+, see LICENSE for more details.
"""

from authlib.specs.oidc import UserInfo
from ._core import OAuthBackend


class Facebook(OAuthBackend):
    OAUTH_TYPE = '2.0'
    OAUTH_NAME = 'facebook'
    OAUTH_CONFIG = {
        'api_base_url': 'https://graph.facebook.com/v2.12',
        'access_token_url': 'https://graph.facebook.com/v2.12/oauth/access_token',
        'authorize_url': 'https://www.facebook.com/v2.12/dialog/oauth',
        'client_kwargs': {'scope': 'email public_profile'},
    }

    def profile(self):
        resp = self.get(
            'me?fields=id,name,'
            'first_name,middle_name,last_name,'
            'email,website,gender,locale'
        )
        resp.raise_for_status()
        data = resp.json()
        params = {
            'sub': str(data['id']),
            'name': data['name'],
            'given_name': data.get('first_name'),
            'family_name': data.get('last_name'),
            'middle_name': data.get('middle_name'),
            'email': data.get('email'),
            'website': data.get('website'),
            'gender': data.get('gender'),
            'locale': data.get('locale')
        }
        return UserInfo(params)
