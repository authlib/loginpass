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
        user_name = self.get_user_name(**kwargs)
        user_email = self.get_user_email(**kwargs)

        params = {
            'sub': user_name['id'],
            'given_name': user_name['firstName'],
            'family_name': user_name['lastName'],
            'name': user_name['firstName'] + ' ' + user_name['lastName'],
            'email': user_email[0],
        }

        return UserInfo(params)

    def get_user_name(self, **kwargs):
        fields = ['id', 'firstName', 'lastName']
        url = 'me?projection=({})'.format(','.join(fields))
        resp = self.get(url, **kwargs)
        resp.raise_for_status()
        user_id = resp.json()['id']
        fname_data = resp.json()['firstName']
        lname_data = resp.json()['lastName']

        def localized_key(name):
            return '{}_{}'.format(
                name['preferredLocale']['language'],
                name['preferredLocale']['country']
            )

        first_name_locale = localized_key(fname_data)
        last_name_locale = localized_key(lname_data)

        return {
            'id': user_id,
            'firstName': fname_data['localized'].get(first_name_locale, ''),
            'lastName': lname_data['localized'].get(last_name_locale, '')
        }

    def get_user_email(self, **kwargs):
        url = 'emailAddress?q=members&projection=(elements*(handle~))'
        resp = self.get(url, **kwargs)
        resp.raise_for_status()

        emails = []
        for el in resp.json().get('elements', []):
            email = el.get('handle~', {}).get('emailAddress')
            if email is not None:
                emails.append(email)

        return emails
