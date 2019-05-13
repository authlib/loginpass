Authlib Loginpass
=================

Social connections powered by [Authlib][]. This library is a part of Authlib project.
It works well with Authlib v0.7+.

[Authlib]: https://authlib.org/

<a href="https://lepture.com/donate"><img src="https://img.shields.io/badge/$-donate-ff69b4.svg?maxAge=2592000" /></a>
<a href="https://patreon.com/lepture"><img src="https://img.shields.io/badge/I0-patreon-f96854.svg?maxAge=2592000" /></a>
<a href="https://travis-ci.org/authlib/loginpass"><img src="https://api.travis-ci.org/authlib/loginpass.svg?branch=master" alt="Build Status"></a>
<a href="https://pypi.org/project/loginpass/"><img src="https://badgen.net/pypi/v/loginpass" alt="PyPI Version"></a>
<a href="https://twitter.com/intent/follow?screen_name=authlib"><img src="https://img.shields.io/twitter/follow/authlib.svg?maxAge=3600&style=social&logo=twitter&label=Follow" alt="Follow Twitter"></a>

```python
from flask import Flask
from authlib.flask.client import OAuth
from loginpass import create_flask_blueprint, GitHub

app = Flask(__name__)
oauth = OAuth(app)

def handle_authorize(remote, token, user_info):
    if token:
        save_token(remote.name, token)
    if user_info:
        save_user(user_info)
        return user_page
    raise some_error

github_bp = create_flask_blueprint(GitHub, oauth, handle_authorize)
app.register_blueprint(github_bp, url_prefix='/github')
```

Useful Links
------------

- Authlib Homepage: <https://authlib.org/>
- Authlib Repository: <https://github.com/lepture/authlib>

Features
--------

Authlib Loginpass contains lots of connections (see below), every connection has a
`profile()` method which returns the same format of user info. It supports OAuth 1,
OAuth 2 and OpenID Connect for now.

The user info that `profile()` returns is standardized with [OpenID Connect UserInfo
claims](http://openid.net/specs/openid-connect-core-1_0.html#StandardClaims),
not something made by me.

Connections
-----------

Connections that Authlib Loginpass contains:

- [x] Google
- [x] GitHub
- [x] Gitlab
- [x] Twitter
- [x] Facebook
- [x] Dropbox
- [x] Reddit
- [x] Linkedin
- [x] Azure
- [x] Discord
- [x] Slack
- [ ] Jira
- [x] StackOverflow
- [x] Bitbucket
- [x] Auth0
- [x] Strava
- [x] Spotify
- [x] Yandex
- [x] Twitch
- [x] VK
- [x] Authlib


Authlib server with authlib loginpass
-----

Client creation for Authlib server

Get Authlib server from here: https://github.com/authlib/example-oauth2-server/pull/46
-  create a virtualenv (from root source folder)
   -  virtualenv venv
   -  source venv/bin/activate
   -  pip3 install -r requirements.txt
-  export AUTHLIB_INSECURE_TRANSPORT=1
-  flask initdb
-  flask run --host=0.0.0.0

Client in auth server should be created as:
-  Client name: whatever_you_want
-  Client URI: http://192.168.1.xx:5000
-  Allowed scope: profile
-  Redirect URI: http://192.168.1.xx:8000/authlib/auth
-  Allowed Grant Types: authorization_code
-  Allowed Response Types: code
-  Token Endpoint Auth Method: client secret basic

After clicking submit, you will get a clientId value and a clientSecret value.  
Copy them to ./loginpass/authlib.py

Usage
-----

Loginpass is just a simple wrapper around [Authlib][], it is configured apps
ready to use with [Flask][] and [Django][]. Checkout the
examples for details.

[Flask]: https://docs.authlib.org/en/latest/client/flask.html
[Django]: https://docs.authlib.org/en/latest/client/django.html

For Flask:
-  copy flask_example/app.py to ./app.py
-  copy flask_example/config.example.py to ./config.py
-  create a virtualenv (from root source folder)
   -  virtualenv venv
   -  source venv/bin/activate
   -  pip3 install -r requirements.txt
-  export AUTHLIB_INSECURE_TRANSPORT=true (if using authlib server)
-  export FLASK_APP=app.py
-  flask run --host=0.0.0.0 --port=8000


License
-------

Loginpass is a group member of Authlib, it is licensed under BSD.
Authlib commercial license applies to this project too, you can get
a commercial license at [Authlib Commercial Plans](https://authlib.org/plans).
