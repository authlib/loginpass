"""
    loginpass.battlenet
    ~~~~~~~~~~~~~~~~

    Loginpass Backend for Battle.net.

    Useful Links:

    - API documentation: https://develop.battle.net/documentation/guides/using-oauth

    :copyright: (c) 2020 by Hsiaoming Yang
    :license: BSD, see LICENSE for more details.
"""


REGION_ENDPOINTS = {
    'us': 'https://us.battle.net/',
    'eu': 'https://eu.battle.net/',
    'kr': 'https://kr.battle.net/',
    'tw': 'https://tw.battle.net/',
    'cn': 'https://www.battlenet.com.cn/',
}


def create_battlenet_backend(name, region='us'):
    if region and region not in REGION_ENDPOINTS:
        raise ValueError('Not a vaild "region"')

    host = REGION_ENDPOINTS[region]
    metadata_url = host + 'oauth/.well-known/openid-configuration'

    class BattleNet(object):
        NAME = name
        OAUTH_CONFIG = {
            'api_base_url': host,
            'server_metadata_url': metadata_url,
            'client_kwargs': {'scope': 'openid wow.profile sc2.profile'},
        }

    return BattleNet


BattleNet = create_battlenet_backend('battlenet', 'us')
