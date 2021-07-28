from ._flask import create_flask_blueprint
from ._apiflask import create_apiflask_blueprint
from ._fastapi import create_fastapi_routes
from ._django import create_django_urlpatterns
from ._consts import version, homepage
from .azure import Azure, create_azure_backend
from .battlenet import BattleNet, create_battlenet_backend
from .google import Google, GoogleServiceAccount
from .github import GitHub
from .facebook import Facebook
from .instagram import Instagram
from .twitter import Twitter
from .dropbox import Dropbox
from .linkedin import LinkedIn
from .reddit import Reddit
from .gitlab import Gitlab, create_gitlab_backend
from .slack import Slack
from .discord import Discord
from .bitbucket import Bitbucket
from .stackapps import StackOverflow, create_stackapps_backend
from .strava import Strava
from .spotify import Spotify
from .yandex import Yandex
from .twitch import Twitch
from .vk import VK
from .line import LINE
from .orcid import ORCiD
from .hydra import create_hydra_backend


__all__ = [
    'create_flask_blueprint',
    'create_apiflask_blueprint',
    'create_fastapi_routes',
    'create_django_urlpatterns',
    'Azure', 'create_azure_backend',
    'BattleNet', 'create_battlenet_backend',
    'Google', 'GoogleServiceAccount',
    'GitHub',
    'Facebook',
    'Instagram',
    'Twitter',
    'Dropbox',
    'LinkedIn',
    'Reddit',
    'Gitlab', 'create_gitlab_backend',
    'Slack',
    'Discord',
    'Bitbucket',
    'StackOverflow', 'create_stackapps_backend',
    'Strava',
    'Spotify',
    'Yandex',
    'Twitch',
    'VK',
    'LINE',
    'ORCiD',
    'create_hydra_backend',
]

__version__ = version
__homepage__ = homepage
