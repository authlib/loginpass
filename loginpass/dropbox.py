"""
    loginpass.dropbox
    ~~~~~~~~~~~~~~~~~

    Loginpass Backend of Dropbox (https://dropbox.com).

    Useful Links:

    - Create App: https://www.dropbox.com/developers/apps
    - API documentation: https://www.dropbox.com/developers/documentation/http/documentation

    :copyright: (c) 2018 by Hsiaoming Yang
    :license: BSD, see LICENSE for more details.
"""


def normalize_userinfo(client, data):
    name_info = data['name']
    params = {
        'sub': data['account_id'],
        'name': name_info.get('display_name'),
        'given_name': name_info.get('given_name'),
        'family_name': name_info.get('surname'),
        'nickname': name_info.get('familiar_name'),
        'email': data.get('email'),
        'email_verified': data.get('email_verified'),
        'locale': data.get('locale'),
        'picture': data.get('profile_photo_url'),
    }
    return params


class Dropbox(object):
    NAME = 'dropbox'
    OAUTH_CONFIG = {
        'api_base_url': 'https://api.dropboxapi.com/2/',
        'access_token_url': 'https://api.dropboxapi.com/oauth2/token',
        'authorize_url': 'https://www.dropbox.com/oauth2/authorize',
        'userinfo_endpoint': 'users/get_current_account',
        'userinfo_compliance_fix': normalize_userinfo,
    }
