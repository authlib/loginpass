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
from ._core import UserInfo, OAuthBackend, map_profile_fields


def vk_compliance_fix(session):
    def _token_response(resp):
        token = resp.json()
        token['token_type'] = 'Bearer'
        resp.json = lambda: token
        return resp

    session.register_compliance_hook('access_token_response', _token_response)


class VK(OAuthBackend):
    OAUTH_TYPE = '2.0'
    OAUTH_NAME = 'vk'
    OAUTH_CONFIG = {
        'api_base_url': 'https://api.vk.com/method/',
        'access_token_url': 'https://oauth.vk.com/access_token',
        'authorize_url': 'https://oauth.vk.com/authorize',
        'client_kwargs': {
            'token_placement': 'uri',
            'token_endpoint_auth_method': 'client_secret_post',
            'scope': 'email'
        },
        'compliance_fix': vk_compliance_fix
    }

    def profile(self, token=None, **kwargs):
        params = {}
        if token and 'email' in token:
            params['email'] = token['email']

        payload = {'v': '5.80', 'fields': 'sex,bdate,has_photo,photo_max_orig,site,screen_name'}
        resp = self.get('users.get', params=payload, token=token, **kwargs)
        resp.raise_for_status()
        data = resp.json()
        params.update(map_profile_fields(data['response'][0], {
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
        }))
        return UserInfo(params)


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
