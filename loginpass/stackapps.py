"""
    loginpass.stackapps
    ~~~~~~~~~~~~~~~~~~~

    Authenticate using `Stack Overflow <https://stackoverflow.com>`_.

    Useful links:

    - Register an application: https://stackapps.com/apps/oauth/register
    - API documentation: https://api.stackexchange.com/

    :copyright: (c) 2018 by Hsiaoming Yang
    :license: BSD, see LICENSE for more details.
"""

from authlib.common.urls import add_params_to_uri, url_decode
from ._core import UserInfo, OAuthBackend, map_profile_fields


def _stackapps_compliance_fix(session, site):
    def _add_extra_info(url, headers, body):
        params = {'site': site}
        api_key = session._kwargs.get('api_key')
        api_filter = session._kwargs.get('api_filter')
        if api_key:
            params['key'] = api_key
        if api_filter:
            params['filter'] = api_filter
        url = add_params_to_uri(url, params)
        return url, headers, body

    def _token_response(resp):
        data = dict(url_decode(resp.text))
        data['token_type'] = 'Bearer'
        data['expires_in'] = int(data['expires'])
        resp.json = lambda: data
        return resp

    session.register_compliance_hook('protected_request', _add_extra_info)
    session.register_compliance_hook('access_token_response', _token_response)


def create_stackapps_backend(name, site):
    """Build StackApps OAuth Backend."""

    authorize_url = 'https://stackoverflow.com/oauth'
    token_url = 'https://stackoverflow.com/oauth/access_token'
    api_base_url = 'https://api.stackexchange.com/2.2'

    class StackApp(OAuthBackend):
        OAUTH_TYPE = '2.0'
        OAUTH_NAME = name
        OAUTH_CONFIG = {
            'api_base_url': api_base_url,
            'access_token_url': token_url,
            'authorize_url': authorize_url,
            'client_kwargs': {
                'token_placement': 'uri',
                'token_endpoint_auth_method': 'client_secret_post',
            },
            'compliance_fix': lambda s: _stackapps_compliance_fix(s, site)
        }
        # you can add api_key, api_filter in client_kwargs

        def profile(self, **kwargs):
            """Get the user's profile."""
            resp = self.get('me', **kwargs)
            resp.raise_for_status()
            data = resp.json()
            return UserInfo(map_profile_fields(data['items'][0], {
                'sub': lambda o: str(o['user_id']),
                'name': 'display_name',
                'preferred_username': 'display_name',
                'profile': 'link',
                'picture': 'profile_image',
                'website': 'website_url',
                'address': 'location',
                'updated_at': 'last_modified_date',
            }))

    return StackApp


StackOverflow = create_stackapps_backend('stackoverflow', 'stackoverflow')
