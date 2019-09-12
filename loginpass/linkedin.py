"""
    loginpass.linkedin
    ~~~~~~~~~~~~~~~~~~

    Loginpass Backend of LinkedIn (https://linkedin.com).

    Useful Links:

    - API documentation: https://developer.linkedin.com/

    :copyright: (c) 2018 by Hsiaoming Yang
    :license: BSD, see LICENSE for more details.
"""

import json
from ._core import UserInfo, OAuthBackend, map_profile_fields


def linkedin_compliance_fix(session):

    def _token_response(resp):
        data = json.loads(resp.text)
        data['token_type'] = 'Bearer'
        resp.json = lambda: data
        return resp

    session.register_compliance_hook('access_token_response', _token_response)


class LinkedIn(OAuthBackend):
    OAUTH_TYPE = '2.0'
    OAUTH_NAME = 'linkedin'
    OAUTH_CONFIG = {
        'api_base_url': 'https://api.linkedin.com/v2/',
        'access_token_url': 'https://www.linkedin.com/oauth/v2/accessToken',
        'authorize_url': 'https://www.linkedin.com/oauth/v2/authorization',
        'client_kwargs': {
            'scope': 'r_liteprofile r_emailaddress',
            'token_endpoint_auth_method': 'client_secret_post',
        },
        'compliance_fix': linkedin_compliance_fix
    }

    def profile(self, **kwargs):
        info = self.get_user_info(**kwargs)
        email = self.get_user_email(**kwargs)
        if email:
            info['email'] = email

        return UserInfo(info)

    def get_user_info(self, **kwargs):
        fields = ['id', 'firstName', 'lastName']
        url = 'me?projection=({})'.format(','.join(fields))
        resp = self.get(url, **kwargs)
        resp.raise_for_status()
        data = resp.json()

        given_name = get_localized_value(data['firstName'])
        family_name = get_localized_value(data['lastName'])
        return {
            'sub': data['id'],
            'given_name': given_name,
            'family_name': family_name,
            'name': ' '.join([given_name, family_name]),
        }

    def get_user_email(self, **kwargs):
        url = 'emailAddress?q=members&projection=(elements*(handle~))'
        resp = self.get(url, **kwargs)
        resp.raise_for_status()
        data = resp.json()

        handle = data.get('handle~')
        if handle:
            return handle.get('emailAddress')


def get_localized_value(name):
    key = '{}_{}'.format(
        name['preferredLocale']['language'],
        name['preferredLocale']['country']
    )
    return name['localized'].get(key, '')
