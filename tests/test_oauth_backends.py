import os
import json
import mock
import unittest
import requests
from loginpass._core import UserInfo
from loginpass import (
    Twitter,
    GitHub,
    Yandex,
    Reddit,
    Dropbox,
)


TEST_DIR = os.path.dirname(os.path.abspath(__file__))


class TestOAuthBackends(unittest.TestCase):
    def run_profile(self, backend, **kwargs):
        filename = '{}_response.json'.format(backend.OAUTH_NAME)
        with open(os.path.join(TEST_DIR, 'data', filename), 'r') as f:
            resp = mock.MagicMock(spec=requests.Response)
            data = json.load(f)
            resp.json = lambda: data
            resp.status_code = 200

        with mock.patch('requests.sessions.Session.send') as send:
            send.return_value = resp
            profile = backend.profile(**kwargs)
            self.assertIsInstance(profile, UserInfo)

        filename = '{}_result.json'.format(backend.OAUTH_NAME)
        with open(os.path.join(TEST_DIR, 'data', filename), 'r') as f:
            result = json.load(f)
            self.assertEqual(dict(profile), result)

    def run_oauth_profile(self, backend_cls):
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
        self.run_profile(c, token=token)

    def test_twitter(self):
        self.run_oauth_profile(Twitter)

    def test_github(self):
        self.run_oauth_profile(GitHub)

    def test_yandex(self):
        self.run_oauth_profile(Yandex)

    def test_reddit(self):
        self.run_oauth_profile(Reddit)

    def test_dropbox(self):
        self.run_oauth_profile(Dropbox)
