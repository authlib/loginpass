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


def normalize_userinfo(client, data):
    return {
        'sub': str(data['id']),
        'name': data['name'],
        'email': data.get('email'),
        'preferred_username': data['username'],
        'profile': data['web_url'],
        'picture': data['avatar_url'],
        'website': data.get('website_url'),
    }


def create_gitlab_backend(name, hostname):
    """Build Gitlab OAuth Backend."""
    api_base_url = 'https://{}/api/v4/'.format(hostname)
    authorize_url = 'https://{}/oauth/authorize'.format(hostname)
    token_url = 'https://{}/oauth/token'.format(hostname)

    class GitlabEE(object):
        NAME = name
        OAUTH_CONFIG = {
            'api_base_url': api_base_url,
            'access_token_url': token_url,
            'authorize_url': authorize_url,
            'userinfo_endpoint': 'user',
            'userinfo_compliance_fix': normalize_userinfo,
            'client_kwargs': {'scope': 'read_user'},
        }

    return GitlabEE


Gitlab = create_gitlab_backend('gitlab', 'gitlab.com')
