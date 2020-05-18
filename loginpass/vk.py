"""
    loginpass.vk
    ~~~~~~~~~~~~~~~~~~~

    Authenticate using `VK <https://vk.com>`_.

    Useful links:

    - Register an application: https://vk.com/editapp?act=create
    - API documentation: https://vk.com/dev/users.get

    :copyright: (c) 2018 by Hsiaoming Yang
    :license: BSD, see LICENSE for more details.
"""

import datetime
from ._core import map_profile_fields


USERINFO_ENDPOINT = (
    'users.get?fields=sex,bdate,has_photo,photo_max_orig,site,screen_name'
    '&v=5.80'
)


def normalize_userinfo(client, data):
    return map_profile_fields(data['response'][0], {
        'sub': lambda o: str(o['id']),
        'name': _get_name,
        'given_name': 'first_name',
        'family_name': 'last_name',
        'preferred_username': 'screen_name',
        'profile': _get_profile,
        'picture': _get_photo,
        'website': 'site',
        'gender': _get_sex,
        'birthdate': _get_bdate
    })


class VK(object):
    NAME = 'vk'
    OAUTH_CONFIG = {
        'api_base_url': 'https://api.vk.com/method/',
        'access_token_url': 'https://oauth.vk.com/access_token',
        'authorize_url': 'https://oauth.vk.com/authorize',
        'client_kwargs': {
            'token_placement': 'uri',
            'token_endpoint_auth_method': 'client_secret_post',
            'scope': 'email'
        },
        'userinfo_endpoint': USERINFO_ENDPOINT,
        'userinfo_compliance_fix': normalize_userinfo,
    }



def _get_name(data):
    return '{} {}'.format(data['first_name'], data['last_name'])


def _get_profile(data):
    return 'https://vk.com/{}'.format(data['screen_name'])


def _get_photo(data):
    has_photo = data['has_photo']
    if has_photo:
        return data['photo_max_orig']


def _get_sex(data):
    sex = data['sex']
    if sex == 1:
        return 'female'
    elif sex == 2:
        return 'male'


def _get_bdate(data):
    bdate = data.get('bdate')
    if bdate:
        try:
            return datetime.datetime.strptime(bdate, '%d.%m.%Y').strftime('%Y-%m-%d')
        except ValueError:
            pass
