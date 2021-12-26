from ._core import map_profile_fields

def normalize_userinfo(client, data):
    return map_profile_fields(data,
    {
        'sub': 'id',
        'email' : 'email',
        'name': 'nickname',
        'given_name': 'first_name',
        'family_name': 'last_name',
        'preferred_username': 'name',
        'picture': "image",
        'gender': 'gender',
        'birthdate': 'birthday'
    })



class MailRu(object):
    NAME = 'mailru'
    OAUTH_CONFIG = {
        'api_base_url': 'https://oauth.mail.ru/',
        'access_token_url': 'https://oauth.mail.ru/token',
        'authorize_url': 'https://oauth.mail.ru/login',
        'userinfo_endpoint': 'https://oauth.mail.ru/userinfo',
        'userinfo_compliance_fix': normalize_userinfo,
        'authorize_params ':
        {
            'scope': 'userinfo'
        },
        'request_token_params':
            {
                'scope': 'userinfo'
            },
        'client_kwargs': {'scope': 'userinfo', 'token_placement': 'uri',}
    }


