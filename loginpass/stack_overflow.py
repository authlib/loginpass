"""
loginpass.stack_overflow
~~~~~~~~~~~~~~~~~~~~~~~~

Authenticate using `Stack Overflow <https://stackoverflow.com>`_.

Useful links:

-   Register an application: https://stackapps.com/apps/oauth/register
-   API documentation: https://api.stackexchange.com/

:copyright: (c) 2018 by Hsiaoming Yang
:license: AGPLv3+, see LICENSE for more details.
"""

from authlib.specs.oidc import UserInfo

from loginpass._core import map_profile_fields
from ._core import OAuthBackend


class StackOverflow(OAuthBackend):
    """Authenticate using Stack Overflow.

    An account can be associated with profiles on multiple Stack
    Exchange sites. The site parameter defaults to ``'stackoverflow'``.

    Requests will return different data based on the filter parameter.
    The default lets the API decide what fields to return.

    Use :meth:`make_backend` to create a backend with different default
    API parameters.
    """

    OAUTH_TYPE = '2.0'
    OAUTH_NAME = 'stack_overflow'
    OAUTH_CONFIG = {
        'authorize_url': 'https://stackoverflow.com/oauth',
        'access_token_url': 'https://stackoverflow.com/oauth/access_token',
        'api_base_url': 'https://api.stackexchange.com/2.2',
        'api_site': 'stackoverflow',
        'api_filter': None,
    }

    def request(self, method, url, token=None, **kwargs):
        # set API parameters if they are not present
        params = kwargs.setdefault('params', {})

        if params.get('site', Ellipsis) is Ellipsis:
            params['site'] = self._kwargs['api_site']

        if params.get('filter', Ellipsis) is Ellipsis:
            params['filter'] = self._kwargs['api_filter']

        return super(StackOverflow, self).request(
            method, url, token=token, **kwargs)

    def profile(self, site=Ellipsis, filter=Ellipsis):
        """Get the user's profile.

        :param site: Query this site instead of the default.
        :param filter: Use this filter instead of the default.
        """
        resp = self.get('me', params={'site': site, 'filter': filter})
        resp.raise_for_status()
        return UserInfo(map_profile_fields(resp.json(), {
            'sub': 'user_id',
            'name': 'display_name',
            'preferred_username': 'display_name',
            'profile': 'link',
            'picture': 'profile_image',
            'website': 'website_url',
            'address': 'location',
            'updated_at': 'last_modified_date',
        }))

    @classmethod
    def make_backend(cls, name, site=None, filter=None, scope=None):
        """Create a backend with different default API parameters.

        For example, to default to the Math site::

            MathSE = StackOverflow.make_backend('MathSE', 'math')

        :param name: Name of newly created class.
        :param site: Default Stack Exchange site to query.
        :param filter: Default filter to use during queries.
        :param scope: Scope to request during authorization.
        """
        config = cls.OAUTH_CONFIG.copy()
        client_kwargs = config['client_kwargs'] = config.get(
            'client_kwargs', {}).copy()

        if site is not None:
            config['api_site'] = site

        if filter is not None:
            config['api_filter'] = filter

        if scope is not None:
            client_kwargs['scope'] = scope

        return type(name, (cls,), {'OAUTH_CONFIG': config})
