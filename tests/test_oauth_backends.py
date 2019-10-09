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
    LinkedIn,
    ORCiD,
    create_hydra_backend
)


TEST_DIR = os.path.dirname(os.path.abspath(__file__))


class TestOAuthBackends(unittest.TestCase):
    def get_profile(self, backend, responses, **kwargs):
        mock_responses = list()
        for filename in responses:
            with open(os.path.join(TEST_DIR, 'data', filename), 'r') as f:
                resp = mock.MagicMock(spec=requests.Response)
                data = json.load(f)
                resp.json.return_value = data
                resp.status_code = 200
                mock_responses.append(resp)

        with mock.patch('requests.sessions.Session.send', side_effect=mock_responses):
            profile = backend.profile(**kwargs)
            self.assertIsInstance(profile, UserInfo)
            return profile

    def run_oauth_profile(self, backend_cls, responses=None, result=None):
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

        if responses is None:
            responses = [c.OAUTH_NAME + '_response.json']

        if result is None:
            result = c.OAUTH_NAME + '_result.json'

        profile = self.get_profile(c, responses, token=token)
        with open(os.path.join(TEST_DIR, 'data', result), 'r') as f:
            rv = json.load(f)
            self.assertEqual(dict(profile), rv)


    def test_battlenet(self):
        self.run_oauth_profile(BattleNet)

    def test_twitter(self):
        self.run_oauth_profile(Twitter)

    def test_github(self):
        self.run_oauth_profile(GitHub)

    def test_github2(self):
        self.run_oauth_profile(
            GitHub,
            ['github2_response1.json', 'github2_response2.json'],
            'github2_result.json',
        )

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

    def test_linkedin(self):
        self.run_oauth_profile(
            LinkedIn,
            ['linkedin_response1.json', 'linkedin_response2.json'],
            'linkedin_result.json',
        )

    def test_orcid(self):
        self.run_oauth_profile(ORCiD)

    def test_hydra(self):
        hydra = create_hydra_backend('hydra', 'localhost')
        self.run_oauth_profile(hydra)
