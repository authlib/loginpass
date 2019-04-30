"""
    loginpass.gitlab
    ~~~~~~~~~~~~~~~~

    Loginpass Backend of Gitlab (https://gitlab.com) and its
    enterprise endpoints.

    Useful Links:

    - API documentation: https://docs.gitlab.com/ee/api/

    :copyright: (c) 2018 by Hsiaoming Yang
    :license: BSD, see LICENSE for more details.
"""

from ._core import UserInfo, OAuthBackend


def create_gitlab_backend(name, hostname):
    """Build Gitlab OAuth Backend."""
    api_base_url = 'https://{hostname}/api/v4/'.format(hostname=hostname)
    authorize_url = 'https://{hostname}/oauth/authorize'.format(hostname=hostname)
    token_url = 'https://{hostname}/oauth/token'.format(hostname=hostname)

    class GitlabEE(OAuthBackend):
        OAUTH_TYPE = '2.0'
        OAUTH_NAME = name
        OAUTH_CONFIG = {
            'api_base_url': api_base_url,
            'access_token_url': token_url,
            'authorize_url': authorize_url,
            'client_kwargs': {'scope': 'read_user'},
        }

        def profile(self, **kwargs):
            resp = self.get('user', **kwargs)
            resp.raise_for_status()
            data = resp.json()
            params = {
                'sub': str(data['id']),
                'name': data['name'],
                'email': data.get('email'),
                'preferred_username': data['username'],
                'profile': data['web_url'],
                'picture': data['avatar_url'],
                'website': data.get('website_url'),
            }
            return UserInfo(params)

        def parse_openid(self, token, nonce=None):
            # https://docs.gitlab.com/ee/integration/openid_connect_provider.html
            # Although Gitlab claims that it support OIDC, the return
            # value doesn't contains the information it claims.
            raise NotImplementedError()

    return GitlabEE


Gitlab = create_gitlab_backend('gitlab', 'gitlab.com')
