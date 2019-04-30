"""
    loginpass.bitbucket
    ~~~~~~~~~~~~~~~~~~~

    Loginpass Backend of Bitbucket (https://bitbucket.org/).

    Useful Links:

    - Create App: https://bitbucket.org/account/
    - API documentation: https://developer.atlassian.com/cloud/bitbucket/

    :copyright: (c) 2018 by Hsiaoming Yang
    :license: BSD, see LICENSE for more details.
"""

from ._core import UserInfo, OAuthBackend, map_profile_fields


class Bitbucket(OAuthBackend):
    OAUTH_TYPE = '2.0'
    OAUTH_NAME = 'bitbucket'
    OAUTH_CONFIG = {
        'api_base_url': 'https://api.bitbucket.org/2.0/',
        'access_token_url': 'https://bitbucket.org/site/oauth2/access_token',
        'authorize_url': 'https://bitbucket.org/site/oauth2/authorize',
        'client_kwargs': {'scope': 'email'},
    }

    def profile(self, **kwargs):
        resp = self.get('user', **kwargs)
        resp.raise_for_status()
        params = map_profile_fields(resp.json(), {
            'sub': 'account_id',
            'name': 'display_name',
            'preferred_username': 'username',
            'address': 'location',
            'website': 'website',
            'picture': _get_avatar,
            'profile': _get_profile,
        })
        resp = self.get('user/emails', **kwargs)
        resp.raise_for_status()
        params.update(_get_email(resp.json()))
        return UserInfo(params)


def _get_profile(data):
    return 'https://bitbucket.org/{}/'.format(data['username'])


def _get_avatar(data):
    avatar = data['links'].get('avatar')
    if avatar:
        return avatar.get('href')


def _get_email(data):
    confirmed_emails = []
    values = data['values']
    for value in values:
        if value['is_primary']:
            return {
                'email': value['email'],
                'email_verified': value['is_confirmed']
            }
        if value['is_confirmed']:
            confirmed_emails.append(value['email'])

    if confirmed_emails:
        return {'email': confirmed_emails[0], 'email_verified': True}

    if values:
        return {'email': values[0], 'email_verified': False}

    return {}
