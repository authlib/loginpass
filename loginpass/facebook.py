from authlib.specs.oidc import UserInfo
from ._core import OAuthBackend


class Facebook(OAuthBackend):
    OAUTH_TYPE = '2.0'
    OAUTH_NAME = 'Facebook'
    OAUTH_CONFIG = {
        'api_base_url': 'https://graph.facebook.com/v2.11',
        'access_token_url': 'https://graph.facebook.com/v2.11/oauth/access_token',
        'authorize_url': 'https://www.facebook.com/v2.11/dialog/oauth',
        'client_kwargs': {'scope': 'email public_profile'},
    }

    def profile(self):
        resp = self.get(
            'me?fields=id,name,'
            'first_name,middle_name,last_name,'
            'email,website,gender,locale'
        )
        data = resp.json()
        params = {
            'sub': str(data['id']),
            'name': data['name'],
            'given_name': data.get('first_name'),
            'family_name': data.get('last_name'),
            'middle_name': data.get('middle_name'),
            'email': data.get('email'),
            'website': data.get('website'),
            'gender': data.get('gender'),
            'locale': data.get('locale')
        }
        return UserInfo(params)
