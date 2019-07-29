"""
    loginpass.b2access
    ~~~~~~~~~~~~~~~~
    Loginpass Backend of B2ACCESS

    gets endpoint from B2ACCESS_API_URL environment variable, if not specified, default development url is used

    development: https://unity.eudat-aai.fz-juelich.de/
    production: https://b2access.eudat.eu).

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

def create_b2access_backend(name,b2accessurl):
    B2ACCESS_API_URL = b2accessurl.strip('/')
    B2ACCESS_TOKEN_URL = '{b2accessurl}/oauth2/token'.format(b2accessurl=b2accessurl)
    B2ACCESS_TOKENINFO_URL = '{b2accessurl}/oauth2/tokeninfo'.format(b2accessurl=b2accessurl)
    B2ACCESS_AUTH_URL = '{b2accessurl}/oauth2-as/oauth2-authz'.format(b2accessurl=b2accessurl)
    B2ACCESS_USERINFO_SUFFIX='/oauth2/userinfo'
    B2ACCESS_USERINFO_URL = '{b2accessurl}/oauth2/userinfo'.format(b2accessurl=b2accessurl)
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

B2Access = create_b2access_backend('b2access','https://b2access.eudat.eu')
B2AccessDev = create_b2access_backend('b2access','https://unity.eudat-aai.fz-juelich.de')
