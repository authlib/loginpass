"""
    loginpass.linkedin
    ~~~~~~~~~~~~~~~~~~

    Loginpass Backend of LinkedIn (https://linkedin.com).

    Useful Links:

    - API documentation: https://developer.linkedin.com/

    :copyright: (c) 2018 by Hsiaoming Yang
    :license: BSD, see LICENSE for more details.
"""


def normalize_userinfo(client, data):
    given_name = get_localized_value(data['firstName'])
    family_name = get_localized_value(data['lastName'])
    params = {
        'sub': data['id'],
        'given_name': given_name,
        'family_name': family_name,
        'name': ' '.join([given_name, family_name]),
    }

    url = 'emailAddress?q=members&projection=(elements*(handle~))'
    resp = client.get(url)
    resp.raise_for_status()
    data = resp.json()

    elements = data.get('elements')
    if elements:
        handle = elements[0].get('handle~')
        if handle:
            email = handle.get('emailAddress')
            if email:
                params['email'] = email
    return params


class LinkedIn(object):
    NAME = 'linkedin'
    OAUTH_CONFIG = {
        'api_base_url': 'https://api.linkedin.com/v2/',
        'access_token_url': 'https://www.linkedin.com/oauth/v2/accessToken',
        'authorize_url': 'https://www.linkedin.com/oauth/v2/authorization',
        'client_kwargs': {
            'scope': 'r_liteprofile r_emailaddress',
            'token_endpoint_auth_method': 'client_secret_post',
        },
        'userinfo_endpoint': 'me?projection=(id,firstName,lastName)',
        'userinfo_compliance_fix': normalize_userinfo,
    }


def get_localized_value(name):
    key = '{}_{}'.format(
        name['preferredLocale']['language'],
        name['preferredLocale']['country']
    )
    return name['localized'].get(key, '')
