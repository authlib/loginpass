from authlib.specs.oidc import UserInfo
from ._core import OAuthBackend


class LinkedIn(OAuthBackend):
    OAUTH_TYPE = '2.0'
    OAUTH_NAME = 'linkedin'
    OAUTH_CONFIG = {
        'api_base_url': 'https://api.linkedin.com/v1/',
        'access_token_url': 'https://www.linkedin.com/uas/oauth2/accessToken',
        'authorize_url': 'https://www.linkedin.com/uas/oauth2/authorization',
        'client_kwargs': {'scope': 'r_basicprofile'},
    }

    def profile(self):
        resp = self.get('people/~')
        data = resp.json()
        # TODO
        params = data
        return UserInfo(params)
