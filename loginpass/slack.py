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

import json
from authlib.common.encoding import to_unicode
from ._core import UserInfo, OAuthBackend


def slack_compliance_fix(session):
    def _fix(resp):
        token = resp.json()
        token['token_type'] = 'Bearer'
        resp._content = to_unicode(json.dumps(token)).encode('utf-8')
        return resp
    session.register_compliance_hook('access_token_response', _fix)


class Slack(OAuthBackend):
    OAUTH_TYPE = '2.0'
    OAUTH_NAME = 'slack'
    # Authlib will always add a client_id in payload
    # When use "client_secret_basic" Slack will report error
    OAUTH_CONFIG = {
        'api_base_url': 'https://slack.com/api/',
        'access_token_url': 'https://slack.com/api/oauth.access',
        'authorize_url': 'https://slack.com/oauth/authorize',
        'client_kwargs': {
            'token_endpoint_auth_method': 'client_secret_post',
            'scope': 'identity.basic identity.avatar identity.email',
        },
        'compliance_fix': slack_compliance_fix
    }

    def profile(self, **kwargs):
        resp = self.get('users.identity', **kwargs)
        data = resp.json()
        resp.raise_for_status()
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
        return UserInfo(params)
