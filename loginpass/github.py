"""
    loginpass.github
    ~~~~~~~~~~~~~~~~

    Loginpass Backend of GitHub (https://github.com).

    Useful Links:

    - Create App: https://github.com/settings/developers
    - API documentation: https://developer.github.com/v3/

    :copyright: (c) 2018 by Hsiaoming Yang
    :license: BSD, see LICENSE for more details.
"""

from ._core import UserInfo, OAuthBackend


class GitHub(OAuthBackend):
    OAUTH_TYPE = '2.0'
    OAUTH_NAME = 'github'
    OAUTH_CONFIG = {
        'api_base_url': 'https://api.github.com/',
        'access_token_url': 'https://github.com/login/oauth/access_token',
        'authorize_url': 'https://github.com/login/oauth/authorize',
        'client_kwargs': {'scope': 'user:email'},
    }

    def profile(self, **kwargs):
        resp = self.get('user', **kwargs)
        resp.raise_for_status()
        data = resp.json()
        params = {
            'sub': str(data['id']),
            'name': data['name'],
            'email': data.get('email'),
            'preferred_username': data['login'],
            'profile': data['html_url'],
            'picture': data['avatar_url'],
            'website': data.get('blog'),
        }

        # The email can be be None despite the scope being 'user:email'.
        # That is because a user can choose to make his/her email private.
        # If that is the case we get all the users emails regardless if private or note
        # and use the one he/she has marked as `primary`
        if params.get("email") is None:
            resp = self.get("user/emails", **kwargs)
            resp.raise_for_status()
            data = resp.json()
            params["email"] = next(email["email"] for email in data if email["primary"])

        return UserInfo(params)
