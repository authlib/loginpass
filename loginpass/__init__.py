from ._core import register_to
from ._flask import create_flask_blueprint
from ._django import create_django_urlpatterns
from ._consts import version, homepage
from .google import Google, GoogleServiceAccount
from .github import GitHub
from .facebook import Facebook
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

__all__ = [
    'register_to',
    'create_flask_blueprint',
    'create_django_urlpatterns',
    'Google', 'GoogleServiceAccount',
    'GitHub',
    'Facebook',
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
]

__version__ = version
__homepage__ = homepage
