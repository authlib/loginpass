"""
    loginpass.slack
    ~~~~~~~~~~~~~~~

    Loginpass Backend of Slack (https://slack.com).

    Useful Links:

    - Create App: https://api.slack.com/apps
    - API documentation: https://api.slack.com/
    - Sign In: https://api.slack.com/docs/sign-in-with-slack

    :copyright: (c) 2018 by Hsiaoming Yang
    :license: BSD, see LICENSE for more details.
"""


def normalize_userinfo(client, data):
    user = data['user']

    picture = None
    for s in ['512', '192', '72', '48', '32', '24']:
        src = user.get('image_' + s)
        if src:
            picture = src
            break

    params = {
        'sub': user['id'],
        'email': user['email'],
        'name': user['name'],
    }
    if picture:
        params['picture'] = picture
    return params


class Slack(object):
    NAME = 'slack'
    OAUTH_CONFIG = {
        'api_base_url': 'https://slack.com/api/',
        'access_token_url': 'https://slack.com/api/oauth.access',
        'authorize_url': 'https://slack.com/oauth/authorize',
        'client_kwargs': {
            'token_endpoint_auth_method': 'client_secret_post',
            'scope': 'identity.basic identity.avatar identity.email',
        },
        'userinfo_endpoint': 'users.identity',
        'userinfo_compliance_fix': normalize_userinfo,
    }
