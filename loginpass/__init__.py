from ._core import register_to, create_flask_blueprint
from ._version import version, homepage
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

__all__ = [
    'register_to', 'create_flask_blueprint',
    'Google', 'GoogleServiceAccount', 'GitHub',
    'Facebook', 'Twitter', 'Dropbox', 'LinkedIn',
    'Reddit', 'Gitlab', 'create_gitlab_backend',
    'Slack', 'Discord',
]

__version__ = version
__homepage__ = homepage
