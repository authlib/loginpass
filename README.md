Authlib Loginpass
=================

Social connections powered by [Authlib][]. This library is a part of Authlib project.
It works well with Authlib v0.7+.

[Authlib]: https://authlib.org/

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

Usage
-----

Loginpass is just a simple wrapper around [Authlib][], it is configured apps
ready to use with [Authlib Client Integrated Frameworks][client]. Checkout the
examples for Flask and Django.

[client]: https://docs.authlib.org/en/latest/client/frameworks.html

License
-------

Loginpass is a group member of Authlib, it is licensed under AGPLv3+.
Authlib commercial license applies to this project too, you can get
a commercial license at [Authlib Commercial Plans](https://authlib.org/plans).
