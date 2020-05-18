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
from ._core import map_profile_fields


def normalize_userinfo(client, data):
    data = data['data']
    return map_profile_fields(data, {
        'sub': lambda o: str(o['id']),
        'name': 'name',
        'given_name': 'full_name',
        'nickname': 'username',
        'picture': 'profile_picture',
        'website': 'website',
    })


class Instagram(object):
    NAME = 'instagram'
    OAUTH_CONFIG = {
        'api_base_url': 'https://api.instagram.com',
        'access_token_url': 'https://api.instagram.com/oauth/access_token',
        'authorize_url': 'https://api.instagram.com/oauth/authorize',
        'client_kwargs': {
            'response_type': 'code',
            'token_endpoint_auth_method': 'client_secret_post',
            'scope': 'basic'
        },
        'userinfo_endpoint': '/v1/users/self',
        'userinfo_compliance_fix': normalize_userinfo,
    }
