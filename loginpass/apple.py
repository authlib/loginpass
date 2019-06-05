"""
    loginpass.apple
    ~~~~~~~~~~~~~~~

    Loginpass Backend of appleid.apple.com.

    Useful Links:

    - API documentation: https://developer.apple.com/documentation/signinwithapplerestapi

    :copyright: (c) 2019 by Corey Burmeister
    :license: BSD, see LICENSE for more details.
"""
from ._core import OAuthBackend, parse_id_token


class Apple(OAuthBackend):
    OAUTH_TYPE = '2.0,oidc'
    OAUTH_NAME = 'apple'
    OAUTH_CONFIG = {
        'api_base_url': 'https://appleid.apple.com/',
        'access_token_url': 'https://appleid.apple.com/auth/token',
        'authorize_url': 'https://appleid.apple.com/auth/authorize',
        'client_kwargs': {
            'response_mode': 'form_post',
            'scope': 'openid email',
        },
    }
    JWK_SET_URL = 'https://appleid.apple.com/auth/keys'

    def profile(self, **kwargs):
        raise NotImplementedError()  # Apple offers no profile resource

    def parse_openid(self, token, nonce=None):
        return parse_id_token(
            self,
            token['id_token'],
            {'iss': {'values': [self.OAUTH_CONFIG['api_base_url']]}},
            token.get('access_token'),
            nonce
        )
