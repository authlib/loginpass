from ._core import register_to
from ._core import create_flask_blueprint, create_django_urlpatterns
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

__all__ = [
    'register_to',
    'create_flask_blueprint',
    'create_django_urlpatterns',
    'Google', 'GoogleServiceAccount', 'GitHub',
    'Facebook', 'Twitter', 'Dropbox', 'LinkedIn',
    'Reddit', 'Gitlab', 'create_gitlab_backend',
    'Slack', 'Discord', 'Bitbucket',
    'StackOverflow', 'create_stackapps_backend',
]

__version__ = version
__homepage__ = homepage
