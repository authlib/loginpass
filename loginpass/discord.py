"""
    loginpass.discord
    ~~~~~~~~~~~~~~~~~

    Loginpass Backend of Discord (https://discordapp.com).

    Useful Links:

    - Create App: https://discordapp.com/developers/applications/me
    - API documentation: https://discordapp.com/developers/docs/reference

    :copyright: (c) 2018 by Hsiaoming Yang
    :license: BSD, see LICENSE for more details.
"""

from ._core import UserInfo, OAuthBackend, map_profile_fields
from ._consts import version, homepage

# see: https://discordapp.com/developers/docs/reference#user-agent
UA = 'Loginpass ({}, {})'.format(homepage, version)


class Discord(OAuthBackend):
    OAUTH_TYPE = '2.0'
    OAUTH_NAME = 'discord'
    OAUTH_CONFIG = {
        'api_base_url': 'https://discordapp.com/api/',
        'access_token_url': 'https://discordapp.com/api/oauth2/token',
        'authorize_url': 'https://discordapp.com/api/oauth2/authorize',
        'client_kwargs': {
            'token_endpoint_auth_method': 'client_secret_post',
            'scope': 'identify email'
        },
    }
    DEFAULT_USER_AGENT = UA

    def profile(self, **kwargs):
        resp = self.get('users/%40me', **kwargs)
        resp.raise_for_status()
        data = resp.json()
        params = map_profile_fields(data, {
            'sub': 'id',
            'name': 'username',
            'email': 'email',
            'preferred_username': 'username',
            'email_verified': 'verified',
        })
        if 'avatar' in data:
            src = 'https://cdn.discordapp.com/avatars/{}/{}.png'
            params['picture'] = src.format(data['id'], data['avatar'])
        return UserInfo(params)
