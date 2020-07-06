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

from ._core import map_profile_fields


def twitch_compliance_fix(session):
    
    # https://discuss.dev.twitch.tv/t/requiring-oauth-for-helix-twitch-api-endpoints/23916
    def fix_protected_request(url, headers, data):
        headers["Client-ID"] = session.client_id
        return url, headers, data


    session.register_compliance_hook(
        'protected_request', fix_protected_request)


def normalize_userinfo(client, data):
    return map_profile_fields(data[0], {
        'sub': 'id',
        'name': 'display_name',
        'preferred_username': 'login',
        'profile': _get_profile,
        'picture': 'profile_image_url',
        'email': 'email',
    })


class Twitch(object):
    NAME = 'twitch'
    OAUTH_CONFIG = {
        'api_base_url': 'https://api.twitch.tv/helix/',
        'access_token_url': 'https://id.twitch.tv/oauth2/token',
        'authorize_url': 'https://id.twitch.tv/oauth2/authorize',
        'client_kwargs': {
            'token_endpoint_auth_method': 'client_secret_post',
            'scope': 'user:read:email'
        },
        'userinfo_endpoint': 'users',
        'userinfo_compliance_fix': normalize_userinfo,
        'compliance_fix': twitch_compliance_fix,
    }


def _get_profile(data):
    return 'https://www.twitch.tv/{}/'.format(data['login'])
