"""
    loginpass.spotify
    ~~~~~~~~~~~~~~~~~~~

    Authenticate using `Spotify <https://www.spotify.com>`_.

    Useful links:

    - Register an application: https://developer.spotify.com/dashboard/applications
    - API documentation: https://developer.spotify.com/documentation/web-api/reference/

    :copyright: (c) 2018 by Hsiaoming Yang
    :license: BSD, see LICENSE for more details.
"""

from ._core import UserInfo, OAuthBackend, map_profile_fields


class Spotify(OAuthBackend):
    OAUTH_TYPE = '2.0'
    OAUTH_NAME = 'spotify'
    OAUTH_CONFIG = {
        'api_base_url': 'https://api.spotify.com/v1/',
        'access_token_url': 'https://accounts.spotify.com/api/token',
        'authorize_url': 'https://accounts.spotify.com/authorize',
        'client_kwargs': {'scope': 'user-read-private user-read-email user-read-birthdate'},
    }

    def profile(self, **kwargs):
        resp = self.get('me', **kwargs)
        resp.raise_for_status()
        data = resp.json()
        params = map_profile_fields(data, {
            'sub': 'id',
            'name': 'display_name',
            'profile': _get_profile,
            'picture': _get_picture,
            'email': 'email',
            'birthdate': 'birthdate',
            'locale': 'country'
        })
        return UserInfo(params)


def _get_profile(data):
    return data['external_urls']['spotify']


def _get_picture(data):
    images = data['images']
    if images:
        return images[0]['url']
