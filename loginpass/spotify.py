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

from ._core import map_profile_fields


def normalize_userinfo(client, data):
    return map_profile_fields(data, {
        'sub': 'id',
        'name': 'display_name',
        'profile': _get_profile,
        'picture': _get_picture,
        'email': 'email',
        'birthdate': 'birthdate',
        'locale': 'country'
    })


class Spotify(object):
    NAME = 'spotify'
    OAUTH_CONFIG = {
        'api_base_url': 'https://api.spotify.com/v1/',
        'access_token_url': 'https://accounts.spotify.com/api/token',
        'authorize_url': 'https://accounts.spotify.com/authorize',
        'client_kwargs': {
            'scope': 'user-read-private user-read-email user-read-birthdate'
        },
        'userinfo_endpoint': 'me',
        'userinfo_compliance_fix': normalize_userinfo,
    }


def _get_profile(data):
    return data['external_urls']['spotify']


def _get_picture(data):
    images = data['images']
    if images:
        return images[0]['url']
