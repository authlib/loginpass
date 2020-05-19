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

from ._core import map_profile_fields


def normalize_userinfo(client, data):
    return map_profile_fields(data, {
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


class Yandex(object):
    NAME = 'yandex'
    OAUTH_CONFIG = {
        'api_base_url': 'https://login.yandex.ru/',
        'access_token_url': 'https://oauth.yandex.com/token',
        'authorize_url': 'https://oauth.yandex.com/authorize',
        'userinfo_endpoint': 'info',
        'userinfo_compliance_fix': normalize_userinfo,
    }


def _get_picture(data):
    if not data.get('is_avatar_empty', True):
        tpl = 'https://avatars.yandex.net/get-yapic/{}/islands-200'
        return tpl.format(data['default_avatar_id'])
