"""
    loginpass.strava
    ~~~~~~~~~~~~~~~~

    Authenticate using `Strava <https://strava.com>`_.

    Useful links:

    - API documentation: https://developers.strava.com/docs/reference/

    :copyright: (c) 2018 by Hsiaoming Yang
"""
from ._core import UserInfo, OAuthBackend, map_profile_fields

authorize_url = 'https://www.strava.com/oauth/authorize'
token_url = 'https://www.strava.com/oauth/token'
api_base_url = 'https://www.strava.com/api/v3/'


class Strava(OAuthBackend):
    OAUTH_TYPE = '2.0'
    OAUTH_NAME = 'strava'
    OAUTH_CONFIG = {
        'api_base_url': api_base_url,
        'access_token_url': token_url,
        'authorize_url': authorize_url,
        'client_kwargs': {
            'response_type': 'code',
            'scope': 'public',
            'token_endpoint_auth_method': 'client_secret_post',
        },
    }

    def profile(self, **kwargs):
        """Get the user's profile."""
        resp = self.get('athlete', **kwargs)
        resp.raise_for_status()
        data = resp.json()
        params = map_profile_fields(data, {
            'name': _compose_name,
            'given_name': 'firstname',
            'family_name': 'lastname',
            'preferred_username': 'username',
            'picture': 'profile',
            'email': 'email',
            'gender': 'sex'
        })
        params['sub'] = str(data['id'])
        return UserInfo(params)


def _compose_name(data):
    return ' '.join((data.get('firstname'), data.get('lastname')))
