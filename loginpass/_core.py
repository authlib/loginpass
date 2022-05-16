def map_profile_fields(data, fields):
    """Copy profile data from site-specific to standard field names.
    Standard keys will only be set if the site data for that key is not
    ``None`` and not empty string.

    :param data: Profile data from the site, to be modified in place.
    :param fields: Map of ``{destination: source}``. Destination is the
        standard name. Source source is the site-specific name, or
        a callable taking ``data`` and returning the value.
    :return: UserInfo fields
    """
    profile = {}
    for dst, src in fields.items():
        if callable(src):
            value = src(data)
        else:
            value = data.get(src)

        if value is not None and value != '':
            profile[dst] = value

    return profile


def oauth_register_remote_app(oauth, backend, **kwargs):
    """Registers & returns an instance of a remote application for 
    the given ``backend`` service.
    
    :param oauth: Authlib OAuth instance
    :param backend: Backend class to register, e.g GitHub, Twitter etc
    :param kwargs: Optional, additional, parameters for Authlib OAuth.register()
    :return: Authlib OAuth remote app
    """
    client_cls = oauth.oauth2_client_cls
    if backend.OAUTH_CONFIG.get('request_token_url'):
        client_cls = oauth.oauth1_client_cls

    class RemoteApp(backend, client_cls):
        OAUTH_APP_CONFIG = backend.OAUTH_CONFIG
    
    return oauth.register(
        RemoteApp.NAME,
        overwrite=True,
        client_cls=RemoteApp,
        **kwargs
    )