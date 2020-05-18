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
