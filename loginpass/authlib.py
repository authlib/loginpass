from ._core import UserInfo, OAuthBackend, map_profile_fields


class Authlib(OAuthBackend):
    OAUTH_TYPE = '2.0'
    OAUTH_NAME = 'authlib'
    OAUTH_CONFIG = {
        'client_id': 'NNZ5uOhjSwzuEZ4S5MQxdf69',
        'client_secret': 'xGGfNfs283CkXmDlMEvpGUxnxeMxvuXVCcWKOLy1xg0sVR3D',
        'api_base_url': 'http://192.168.1.83:5000/',
        'access_token_url': 'http://192.168.1.83:5000/oauth/token',
        'authorize_url': 'http://192.168.1.83:5000/oauth/authorize',
        'client_kwargs': {
            'scope': 'profile',
            'token_endpoint_auth_method': 'client_secret_basic',
        },
    }

    def profile(self, **kwargs):
        if 'params' not in kwargs:
            fields = [
                'id', 'name', 'first_name', 'middle_name', 'last_name',
                'email', 'website', 'gender', 'locale'
            ]
            kwargs['params'] = {'fields': ','.join(fields)}
        resp = self.get('api/me', **kwargs)
        resp.raise_for_status()
        return UserInfo(**resp.json())
