from authlib.specs.rfc7519 import JWT
from authlib.specs.oidc import CodeIDToken, UserInfo
from ._core import OAuthBackend


GOOGLE_API_URL = 'https://www.googleapis.com/'
GOOGLE_TOKEN_URL = GOOGLE_API_URL + 'oauth2/v4/token'
GOOGLE_JWK_URL = GOOGLE_API_URL + 'oauth2/v3/certs'
GOOGLE_AUTH_URL = (
    'https://accounts.google.com/o/oauth2/v2/auth'
    '?access_type=offline'
)
GOOGLE_CLAIMS_OPTIONS = {
    "iss": {
        "values": ['https://accounts.google.com', 'accounts.google.com']
    }
}


class Google(OAuthBackend):
    OAUTH_TYPE = '2'
    OAUTH_NAME = 'google'
    OAUTH_CONFIG = {
        'api_base_url': GOOGLE_API_URL,
        'access_token_url': GOOGLE_TOKEN_URL,
        'authorize_url': GOOGLE_AUTH_URL,
        'client_kwargs': {'scope': 'openid email profile'},
    }
    JWK_SET_URL = GOOGLE_JWK_URL

    def profile(self):
        resp = self.get('oauth2/v3/userinfo')
        return UserInfo(**resp.json())

    def parse_openid(self, response, nonce=None):
        jwk_set = self.fetch_jwk_set()
        id_token = response['id_token']
        claims_params = dict(
            nonce=nonce,
            client_id=self.client_id,
            access_token=response['access_token']
        )
        jwt = JWT()
        claims = jwt.decode(
            id_token, key=jwk_set,
            claims_cls=CodeIDToken,
            claims_options=GOOGLE_CLAIMS_OPTIONS,
            claims_params=claims_params,
        )
        claims.validate(leeway=120)
        return UserInfo(claims)
