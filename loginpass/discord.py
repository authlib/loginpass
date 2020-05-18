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

from ._core import map_profile_fields
from ._consts import version, homepage

# see: https://discordapp.com/developers/docs/reference#user-agent
UA = 'Loginpass ({}, {})'.format(homepage, version)


def normalize_userinfo(client, data):
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
    return params


class Discord(object):
    NAME = 'discord'
    OAUTH_CONFIG = {
        'api_base_url': 'https://discordapp.com/api/',
        'access_token_url': 'https://discordapp.com/api/oauth2/token',
        'authorize_url': 'https://discordapp.com/api/oauth2/authorize',
        'userinfo_endpoint': 'https://discordapp.com/api/users/%40me',
        'userinfo_compliance_fix': normalize_userinfo,
        'client_kwargs': {
            'token_endpoint_auth_method': 'client_secret_post',
            'scope': 'identify email'
        },
    }
    DEFAULT_USER_AGENT = UA
