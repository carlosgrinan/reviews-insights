import os

import requests
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from . import http
from googleapiclient.discovery import build

TOKEN_URI = "https://oauth2.googleapis.com/token"


class GoogleApi:
    def __init__(
        self,
        api_name,
        api_version,
        refresh_token,
        # mock=False,
        # mock_filename=None
    ):
        load_dotenv()

        # if mock:
        #     http = HttpMock(mock_filename, {"status": "200"})
        #     self.service = build(api_name, api_version, http=http)

        # else:
        credentials = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri=TOKEN_URI,
            client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("CLIENT_SECRET"),
        )
        self.service = build(api_name, api_version, credentials=credentials)

    def new_batch_http_request(
        self,
    ):
        """
        Same as service.new_batch_http_request() but returns a BatchHttpRequestCustom"""
        batch = self.service.new_batch_http_request()
        return http.BatchHttpRequestCustom(batch)


def code_to_token(code):
    url = TOKEN_URI
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "redirect_uri": "http://127.0.0.1:8069",  # One of the redirect URIs listed for your project in the API Console Credentials page for the given client_id. Not used but required.
    }
    response = requests.post(url, data=data)
    return response.json().get("refresh_token")
