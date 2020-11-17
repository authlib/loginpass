"""
    loginpass.trello
    ~~~~~~~~~~~~~~~~~
    Loginpass Backend of Trello (https://trello.com).
    Useful Links:
    - Create App: https://trello.com/app-key
    - API documentation: https://developer.atlassian.com/cloud/trello/guides/rest-api/authorization/
    :copyright: (c) 2018 by Hsiaoming Yang
    :license: BSD, see LICENSE for more details.
"""

def normalize_userinfo(client, data):
  params = {
      "sub": data["id"],
      "name": data["fullName"],
      "email": data.get("email"),
      "picture": data.get("avatarUrl"),
      "preferred_username": data.get("username"),
      "profile": data.get("url"),
  }
  return params


class Trello(object):
    NAME = "trello"
    OAUTH_CONFIG = {
        "api_base_url": "https://api.trello.com/1/",
        "request_token_url": "https://trello.com/1/OAuthGetRequestToken",
        "access_token_url": "https://trello.com/1/OAuthGetAccessToken",
        "authorize_url": "https://trello.com/1/OAuthAuthorizeToken",
        "userinfo_endpoint": "members/me/",
        "userinfo_compliance_fix": normalize_userinfo,
    }
