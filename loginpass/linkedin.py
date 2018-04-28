"""
    loginpass.linkedin
    ~~~~~~~~~~~~~~~~~~

    Loginpass Backend of LinkedIn (https://linkedin.com).

    Useful Links:

    - API documentation: https://developer.linkedin.com/

    :copyright: (c) 2018 by Hsiaoming Yang
    :license: AGPLv3+, see LICENSE for more details.
"""

from authlib.specs.oidc import UserInfo
from ._core import OAuthBackend, map_profile_fields


class LinkedIn(OAuthBackend):
    OAUTH_TYPE = '2.0'
    OAUTH_NAME = 'linkedin'
    OAUTH_CONFIG = {
        'api_base_url': 'https://api.linkedin.com/v1/',
        'access_token_url': 'https://www.linkedin.com/oauth/v2/accessToken',
        'authorize_url': 'https://www.linkedin.com/oauth/v2/authorization',
        'client_kwargs': {'scope': 'r_basicprofile r_emailaddress'},
    }

    def profile(self, **kwargs):
        fields = [
            'id', 'email-address', 'picture-url', 'public-profile-url',
            'formatted-name', 'first-name', 'last-name', 'maiden-name',
        ]
        url = 'people/~:({})'.format(','.join(fields))
        resp = self.get(url, **kwargs)
        resp.raise_for_status()
        return UserInfo(map_profile_fields(resp.json(), {
            'sub': 'id',
            'email': 'emailAddress',
            'name': 'formattedName',
            'given_name': 'firstName',
            'family_name': 'lastName',
            'middle_name': 'maidenName',
            'picture': 'pictureUrl',
            'profile': 'publicProfileUrl',
        }))
