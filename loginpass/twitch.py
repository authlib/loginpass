"""
    loginpass.twitch
    ~~~~~~~~~~~~~~~~~~~

    Authenticate using `Twitch <https://www.twitch.tv>`_.

    Useful links:

    - Register an application: https://glass.twitch.tv/console/apps
    - API documentation: https://dev.twitch.tv/docs/api/reference/#get-users

    :copyright: (c) 2018 by Hsiaoming Yang
    :license: BSD, see LICENSE for more details.
"""

from ._core import UserInfo, OAuthBackend, map_profile_fields


class Twitch(OAuthBackend):
    OAUTH_TYPE = '2.0'
    OAUTH_NAME = 'twitch'
    OAUTH_CONFIG = {
        'api_base_url': 'https://api.twitch.tv/helix/',
        'access_token_url': 'https://id.twitch.tv/oauth2/token',
        'authorize_url': 'https://id.twitch.tv/oauth2/authorize',
        'client_kwargs': {
            'token_endpoint_auth_method': 'client_secret_post',
            'scope': 'user:read:email'
        },
    }

    def profile(self, **kwargs):
        resp = self.get('users', **kwargs)
        resp.raise_for_status()
        data = resp.json()['data'][0]
        params = map_profile_fields(data, {
            'sub': 'id',
            'name': 'display_name',
            'preferred_username': 'login',
            'profile': _get_profile,
            'picture': 'profile_image_url',
            'email': 'email',
        })
        return UserInfo(params)


def _get_profile(data):
    return 'https://www.twitch.tv/{}/'.format(data['login'])
