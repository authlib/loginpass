from authlib.specs.oidc import UserInfo
from ._core import OAuthBackend, map_profile_fields

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
            'response_type': 'code', 'scope': 'public', 'token_endpoint_auth_method': 'client_secret_post',
        },
    }

    def profile(self, **kwargs):
        """Get the user's profile."""
        resp = self.get('athlete', **kwargs)
        resp.raise_for_status()
        data = resp.json()
        params = map_profile_fields(data, {
            'sub': 'id',
            'name': 'username',
            'given_name': 'firstname',
            'family_name': 'lastname',
            'preferred_username': 'username',
            'profile': 'profile',
            'picture': 'profile_medium',
            'email': 'email',
            'gender': 'sex'
        })
        return UserInfo(params)
