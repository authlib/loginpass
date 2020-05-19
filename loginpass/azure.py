"""
    loginpass.azure
    ~~~~~~~~~~~~~~~

    Loginpass Backend of Azure AD.

    :copyright: (c) 2018 by Hsiaoming Yang
    :license: BSD, see LICENSE for more details.
"""


def create_azure_backend(name, tenant, version=2):

    base_url = 'https://login.microsoftonline.com/common/'
    if version == 1:
        metadata_url = base_url + '.well-known/openid-configuration'
    elif version == 2:
        metadata_url = base_url + 'v2.0/.well-known/openid-configuration'
    else:
        raise ValueError('Invalid version value')

    class AzureAD(object):
        NAME = name
        OAUTH_CONFIG = {
            'api_base_url': 'https://graph.microsoft.com/',
            'server_metadata_url': metadata_url,
            'client_kwargs': {'scope': 'openid email profile'},
        }

        def load_server_metadata(self):
            metadata = super(AzureAD, self).load_server_metadata()
            # fix issuer value
            issuer = metadata['issuer']
            issuer = issuer.replace('{tenantid}', tenant)
            metadata['issuer'] = issuer
            return metadata

    return AzureAD


Azure = create_azure_backend('azure', 'common')
