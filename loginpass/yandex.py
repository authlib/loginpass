"""
    loginpass.yandex
    ~~~~~~~~~~~~~~~~~~~

    Authenticate using `Yandex <https://yandex.com/>`_.

    Useful links:

    - Register an application: https://oauth.yandex.com/client/new
    - API documentation: https://tech.yandex.com/passport/doc/dg/reference/response-docpage/

    :copyright: (c) 2018 by Hsiaoming Yang
    :license: BSD, see LICENSE for more details.
"""

from ._core import UserInfo, OAuthBackend, map_profile_fields


class Yandex(OAuthBackend):
    OAUTH_TYPE = '2.0'
    OAUTH_NAME = 'yandex'
    OAUTH_CONFIG = {
        'api_base_url': 'https://login.yandex.ru/',
        'access_token_url': 'https://oauth.yandex.com/token',
        'authorize_url': 'https://oauth.yandex.com/authorize',
    }

    def profile(self, **kwargs):
        resp = self.get('info', **kwargs)
        resp.raise_for_status()
        data = resp.json()
        params = map_profile_fields(data, {
            'sub': 'id',
            'name': 'real_name',
            'given_name': 'first_name',
            'family_name': 'last_name',
            'preferred_username': 'login',
            'picture': _get_picture,
            'email': 'default_email',
            'gender': 'sex',
            'birthdate': 'birthday'
        })
        return UserInfo(params)


def _get_picture(data):
    if not data.get('is_avatar_empty', True):
        tpl = 'https://avatars.yandex.net/get-yapic/{}/islands-200'
        return tpl.format(data['default_avatar_id'])
