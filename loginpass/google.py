"""
    loginpass.google
    ~~~~~~~~~~~~~~~~

    This module contains a loginpass backend of Google,
    and a ServiceAccount requests Session.

    :copyright: (c) 2018 by Hsiaoming Yang
    :license: BSD, see LICENSE for more details.
"""

import json
from authlib.integrations.requests_client import AssertionSession


GOOGLE_API_URL = 'https://www.googleapis.com/'
METADATA_URL = 'https://accounts.google.com/.well-known/openid-configuration'


class Google(object):
    NAME = 'google'
    OAUTH_CONFIG = {
        'api_base_url': GOOGLE_API_URL,
        'server_metadata_url': METADATA_URL,
        'client_kwargs': {'scope': 'openid email profile'},
    }


class GoogleServiceAccount(AssertionSession):
    @classmethod
    def from_service_account_file(cls, conf_file, scope, subject=None):
        with open(conf_file, 'r') as f:
            conf = json.load(f)

        token_url = conf['token_uri']
        issuer = conf['client_email']
        key = conf['private_key']
        key_id = conf.get('private_key_id')

        header = {'alg': 'RS256'}
        if key_id:
            header['kid'] = key_id

        # Google puts scope in payload
        claims = {'scope': scope}
        return cls(
            grant_type=cls.JWT_BEARER_GRANT_TYPE,
            token_url=token_url,
            issuer=issuer,
            audience=token_url,
            claims=claims,
            subject=subject,
            key=key,
            header=header,
        )
