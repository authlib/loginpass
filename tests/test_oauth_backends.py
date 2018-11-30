import os
import json
import mock
import requests
from loginpass._core import UserInfo
from loginpass import (
    Twitter,
    GitHub,
    Yandex,
)


TEST_DIR = os.path.dirname(os.path.abspath(__file__))


def run_profile(backend, **kwargs):
    filename = '{}_response.json'.format(backend.OAUTH_NAME)
    with open(os.path.join(TEST_DIR, 'data', filename), 'r') as f:
        resp = mock.MagicMock(spec=requests.Response)
        data = json.load(f)
        resp.json = lambda: data
        resp.status_code = 200

    with mock.patch('requests.sessions.Session.send') as send:
        send.return_value = resp
        profile = backend.profile(**kwargs)
        assert isinstance(profile, UserInfo)

    filename = '{}_result.json'.format(backend.OAUTH_NAME)
    with open(os.path.join(TEST_DIR, 'data', filename), 'r') as f:
        result = json.load(f)
        assert dict(profile) == result


def run_oauth_profile(backend_cls):
    c = backend_cls(
        client_id='a',
        client_secret='b',
        **backend_cls.OAUTH_CONFIG
    )
    if c.OAUTH_TYPE == '1.0':
        token = {
            'oauth_token': 'a',
            'oauth_token_secret': 'b'
        }
    else:
        token = {
            'token_type': 'bearer',
            'access_token': 'a'
        }
    run_profile(c, token=token)


def test_twitter():
    run_oauth_profile(Twitter)


def test_github():
    run_oauth_profile(GitHub)


def test_yandex():
    run_oauth_profile(Yandex)
