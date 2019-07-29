"""
    loginpass.b2access
    ~~~~~~~~~~~~~~~~
    Loginpass Backend of B2ACCESS

    gets endpoint from B2ACCESS_API_URL environment variable, if not specified, default development url is used

    development: https://unity.eudat-aai.fz-juelich.de/
    production: https://b2access.eudat.eu/

    :copyright: (c) 2019 by Tomas Kulhanek, ESDF
    :license: MIT, see LICENSE for more details.

"""

from loginpass._core import UserInfo, OAuthBackend
import os

#Authorization Grant 	https://unity.eudat-aai.fz-juelich.de:443/oauth2-as/oauth2-authz 	https://b2access.eudat.eu:443/oauth2-as/oauth2-authz
#Access Token 	https://unity.eudat-aai.fz-juelich.de:443/oauth2/token 	https://b2access.eudat.eu:443/oauth2/token
#Token Information/validation 	https://unity.eudat-aai.fz-juelich.de:443/oauth2 /tokeninfo 	https://b2access.eudat.eu:443/oauth2/tokeninfo
#User information 	https://unity.eudat-aai.fz-juelich.de:443/oauth2/userinfo 	https://b2access.eudat.eu:443/oauth2/userinfo

# development endpoint
B2ACCESS_API_URL = os.environ.get('B2ACCESS_API_URL',default='https://unity.eudat-aai.fz-juelich.de/')
B2ACCESS_TOKEN_URL = B2ACCESS_API_URL + 'oauth2/token'
B2ACCESS_TOKENINFO_SUFFIX='oauth2/tokeninfo'
B2ACCESS_TOKENINFO_URL = B2ACCESS_API_URL + B2ACCESS_TOKENINFO_SUFFIX
B2ACCESS_AUTH_URL = B2ACCESS_API_URL + 'oauth2-as/oauth2-authz'
B2ACCESS_USERINFO_SUFFIX='oauth2/userinfo'
B2ACCESS_USERINFO_URL = B2ACCESS_API_URL + B2ACCESS_USERINFO_SUFFIX

class B2Access(OAuthBackend):
    OAUTH_TYPE = '2.0,oidc'
    OAUTH_NAME = 'b2access'
    OAUTH_CONFIG = {
        'api_base_url': B2ACCESS_API_URL,
        'access_token_url': B2ACCESS_TOKEN_URL,
        'authorize_url': B2ACCESS_AUTH_URL,
        'client_kwargs': {'scope': 'email profile'},
    }

    def profile(self, **kwargs):
        print('b2access profile kwargs:',kwargs)
        resp = self.get(B2ACCESS_USERINFO_SUFFIX,**kwargs)
        data = resp.json()
        params = {
            'sub': data['sub'],
            'name': data['name'],
            'email': data['email'],
        }
        return UserInfo(params)
