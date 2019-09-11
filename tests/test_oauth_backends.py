import os
import json
import mock
import unittest
import requests
from loginpass._core import UserInfo
from loginpass import (
    BattleNet,
    Twitter,
    GitHub,
    Yandex,
    Reddit,
    Dropbox,
    Discord,
    Twitch,
    Gitlab,
    Strava,
    ORCiD,
)


TEST_DIR = os.path.dirname(os.path.abspath(__file__))


class TestOAuthBackends(unittest.TestCase):
    def run_profile(self, backend, **kwargs):
        mock_responses = list()
        test_backend_dir = os.path.join(TEST_DIR, 'data', backend.OAUTH_NAME)

        # We are only interested in the root level files of this directory.
        (_, _, filenames) = next(os.walk(test_backend_dir))
        response_files = sorted(r for r in filenames if '_response.json' in r)
        for rf in response_files:
            resp = mock.MagicMock(spec=requests.Response)
            with open(os.path.join(test_backend_dir, rf), 'r') as f:
                data = json.load(f)
            resp.json.return_value = data
            resp.status_code = 200
            mock_responses.append(resp)

        with mock.patch('requests.sessions.Session.send', side_effect=mock_responses):
            profile = backend.profile(**kwargs)
            self.assertIsInstance(profile, UserInfo)

        filename = 'result.json'
        with open(os.path.join(test_backend_dir, filename), 'r') as f:
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

    def test_battlenet(self):
        self.run_oauth_profile(BattleNet)

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

    def test_discord(self):
        self.run_oauth_profile(Discord)

    def test_twitch(self):
        self.run_oauth_profile(Twitch)

    def test_gitlab(self):
        self.run_oauth_profile(Gitlab)

    def test_strava(self):
        self.run_oauth_profile(Strava)

    def test_orcid(self):
        self.run_oauth_profile(ORCiD)
