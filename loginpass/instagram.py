"""
    loginpass.instagram
    ~~~~~~~~~~~~~~~~~~

    Loginpass Backend of Instagram (instagram.com)

    Useful Links:
    - Dev Portal: https://www.instagram.com/developer/
    - Apps need to be reviewed: https://www.instagram.com/developer/review/


    :copyright: (c) 2019 by Ruben Di Battista
    :license: BSD, see LICENSE for more details.
"""
from ._core import UserInfo, OAuthBackend, map_profile_fields


def instagram_compliance_fix(session):
    def _token_response(resp):
        token = resp.json()
        token['token_type'] = 'Bearer'
        resp.json = lambda: token
        return resp

    session.register_compliance_hook('access_token_response', _token_response)


class Instagram(OAuthBackend):
    OAUTH_TYPE = '2.0'
    OAUTH_NAME = 'instagram'
    OAUTH_CONFIG = {
        'api_base_url': 'https://api.instagram.com',
        'access_token_url': 'https://api.instagram.com/oauth/access_token',
        'authorize_url': 'https://api.instagram.com/oauth/authorize',
        'client_kwargs': {
            'response_type': 'code',
            'token_endpoint_auth_method': 'client_secret_post',
            'scope': 'basic'
        },
        'compliance_fix': instagram_compliance_fix
    }

    def profile(self, token=None, **kwargs):
        data = None
        if token is not None:
            data = token.get('user')

        if data is None:
            resp = self.get('/v1/users/self', **kwargs)
            resp.raise_for_status()
            data = resp.json()['data']
        return UserInfo(map_profile_fields(data, {
            'sub': lambda o: str(o['id']),
            'name': 'name',
            'given_name': 'full_name',
            'nickname': 'username',
            'picture': 'profile_picture',
            'website': 'website',
        }))
