"""
    loginpass.battlenet
    ~~~~~~~~~~~~~~~~

    Loginpass Backend for Battle.net.

    Useful Links:

    - API documentation: https://develop.battle.net/documentation/guides/using-oauth

    :copyright: (c) 2019 by Corey Burmeister
    :license: BSD, see LICENSE for more details.
"""
from loginpass._core import OAuthBackend, UserInfo


class BattleNet(OAuthBackend):
    OAUTH_TYPE = '2.0'
    OAUTH_NAME = 'battlenet'
    OAUTH_CONFIG = {
        'api_base_url': 'https://us.battle.net/',
        'access_token_url': 'https://us.battle.net/oauth/token',
        'authorize_url': 'https://us.battle.net/oauth/authorize',
        'client_kwargs': {'scope': 'wow.profile sc2.profile'},
    }

    def profile(self, **kwargs):
        resp = self.get('oauth/userinfo', **kwargs)
        resp.raise_for_status()
        data = resp.json()
        return UserInfo(data)
