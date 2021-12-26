
'''
{"birthday": "20.12.1985", "client_id": "eb986c7d5ed6403888f9f21fbc61472e", "email": "vladimir.kuzovkin@bk.ru",
 "first_name": "\u0412\u043b\u0430\u0434\u0438\u043c\u0438\u0440", "gender": "m", "id": "566178036",
 "image": "https://filin.mail.ru/pic?d=0X8q6bJrl-rjR88OIE5UuCjmcVX-RaQr8TET95nPRQR8xgSC_oNyfVQUjaRxSKVrHGukgZc~&width=180&height=180",
 "last_name": "\u041a\u0443\u0437\u043e\u0432\u043a\u0438\u043d", "locale": "ru_RU",
 "name": "\u0412\u043b\u0430\u0434\u0438\u043c\u0438\u0440 \u041a\u0443\u0437\u043e\u0432\u043a\u0438\u043d",
 "nickname": "\u0412\u043b\u0430\u0434\u0438\u043c\u0438\u0440 \u041a\u0443\u0437\u043e\u0432\u043a\u0438\u043d"}
'''


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
    }




