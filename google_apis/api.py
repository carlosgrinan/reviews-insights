import os

import requests
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from googleapiclient.http import HttpMock
from .http import BatchHttpRequestCustom

TOKEN_URI = "https://oauth2.googleapis.com/token"


class GoogleApi:
    def __init__(self, api_name, api_version, refresh_token, mock=False, mock_filename=None, **kwargs):
        if mock:
            http = HttpMock(mock_filename, {"status": "200"})
            self.service = build(api_name, api_version, http=http, **kwargs)

        else:
            load_dotenv()
            credentials = Credentials(
                token=None,
                refresh_token=refresh_token,
                token_uri=TOKEN_URI,
                client_id=os.getenv("CLIENT_ID"),
                client_secret=os.getenv("CLIENT_SECRET"),
            )
            self.service = build(api_name, api_version, credentials=credentials, **kwargs)

    def new_batch_http_request(
        self,
    ):
        """
        Same as ``self.service.new_batch_http_request()`` but returns a ``BatchHttpRequestCustom``"""
        batch = self.service.new_batch_http_request()
        return BatchHttpRequestCustom(batch)


def code_to_token(code):
    """
    Returns a refresh token given an authorization code.
    """
    load_dotenv()
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "redirect_uri": "http://127.0.0.1:8069",  # Has to match the redirect URI used to get the authorization code. If authorization code ux_mode was popup, has to match the URI from which the auth flow was initiated. Beware of using localhost and 127.0.0.1, because they are not the same for Google.
    }
    response = requests.post(TOKEN_URI, data=data)
    return response.json().get("refresh_token")
