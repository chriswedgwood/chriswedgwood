from django.test import TestCase
from instagramgobbler.views import get_short_lived_token
from unittest.mock import patch


class InstagramGobblerViewTests(TestCase):
    def setUp(self):
        self.code = "ABCDE"

    def test_gobble(self):
        assert "gobble" == "gobble"

    @patch("instagramgobbler.views.requests.post")
    def test_getting_short_token(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = """{"token": "abcde"}"""
        json_response = get_short_lived_token(self.code)
        assert json_response == {"token": "abcde"}

    @patch("instagramgobbler.views.requests.post")
    def test_getting_short_token_failed_call(self, mock_post):
        mock_post.return_value.status_code = 400
        mock_post.return_value.text = """{"error": "something bad happened"}"""
        json_response = get_short_lived_token(self.code)
        assert json_response is None
