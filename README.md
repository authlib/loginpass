Authlib Loginpass
=================

Social connections powered by [Authlib][]. This library is a part of Authlib project.
It works well with Authlib v0.14.3+.

[Authlib]: https://authlib.org/

<a href="https://lepture.com/donate"><img src="https://img.shields.io/badge/$-donate-ff69b4.svg?maxAge=2592000" /></a>
<a href="https://patreon.com/lepture"><img src="https://img.shields.io/badge/I0-patreon-f96854.svg?maxAge=2592000" /></a>
<a href="https://travis-ci.org/authlib/loginpass"><img src="https://api.travis-ci.org/authlib/loginpass.svg?branch=master" alt="Build Status"></a>
<a href="https://pypi.org/project/loginpass/"><img src="https://badgen.net/pypi/v/loginpass" alt="PyPI Version"></a>
<a href="https://twitter.com/intent/follow?screen_name=authlib"><img src="https://img.shields.io/twitter/follow/authlib.svg?maxAge=3600&style=social&logo=twitter&label=Follow" alt="Follow Twitter"></a>

```python
from flask import Flask
from authlib.integrations.flask_client import OAuth
from loginpass import create_flask_blueprint
from loginpass import Twitter, GitHub, Google

app = Flask(__name__)
oauth = OAuth(app)

def handle_authorize(remote, token, user_info):
    if token:
        save_token(remote.name, token)
    if user_info:
        save_user(user_info)
        return user_page
    raise some_error

backends = [Twitter, GitHub, Google]
bp = create_flask_blueprint(backends, oauth, handle_authorize)
app.register_blueprint(bp, url_prefix='')
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

- [x] Battle.net
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
- [x] [Ory Hydra](https://www.ory.sh/docs/hydra/)

Usage
-----

Loginpass is just a simple wrapper around [Authlib][], it is configured apps
ready to use with [Flask][] and [Django][]. Checkout the
examples for details.

[Flask]: https://docs.authlib.org/en/latest/client/flask.html
[Django]: https://docs.authlib.org/en/latest/client/django.html

License
-------

Loginpass is a group member of Authlib, it is licensed under BSD.
Authlib commercial license applies to this project too, you can get
a commercial license at [Authlib Commercial Plans](https://authlib.org/plans).
