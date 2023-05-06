import os
from pprint import pprint
import googlemaps
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import HttpMock

from google.gmail.utils import get_text
from google.http import BatchHttpRequestCustom


class GoogleApi:
    def __init__(
        self,
        api_name,
        api_version,
        refresh_token,
        # mock=False,
        # mock_filename=None
    ):
        # if mock:
        #     http = HttpMock(mock_filename, {"status": "200"})
        #     self.service = build(api_name, api_version, http=http)

        # else:
        credentials = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
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
        return BatchHttpRequestCustom(batch)


class Gmail(GoogleApi):
    def __init__(
        self,
        refresh_token,
        #  mock=False
    ):
        super().__init__(
            "gmail",
            "v1",
            refresh_token,
            #  mock=mock,
            #  mock_filename="",
        )

    def get_emails(self, mock=False):
        """
        Returns a list of emails texts
        """
        if mock:
            http_mock = HttpMock("mock_data/messages-list.json", {"status": "200"})
            # http_batch_mock = ...
        else:
            http_mock = None
            # http_batch_mock = None

        response = (
            self.service.users()
            .messages()
            .list(
                userId="me",
                labelIds=["INBOX"],
                maxResults=10,
                q="-is:forward -is:reply",
                fields="messages/id",
            )
            .execute(http=http_mock)
        )
        pprint(response)
        minimal_messages = response.get("messages", [])

        # list() doesn't return the body of the messages, so now we need to get the
        # messages one by one:
        batch = self.new_batch_http_request()
        for minimal_message in minimal_messages:
            request = (
                self.service.users()
                .messages()
                .get(
                    userId="me",
                    id=minimal_message["id"],
                    format="full",
                    fields="payload",
                )
            )
            batch.add(request)
        messages = batch.execute(
            # http=http_batch_mock
        )

        emails_text = [get_text(message) for message in messages]
        emails_text = [text for text in emails_text if text]  # remove empty strings
        return emails_text


def google_maps(place_id="ChIJN1t_tDeuEmsRUsoyG83frY4"):
    gmaps = googlemaps.Client(key=os.getenv("GOOGLE_API_KEY"))
    response = gmaps.place(
        place_id,
        fields=["reviews"],
        language="en",
        reviews_sort="most_relevant",
    )
    reviews = response["result"].get("reviews", [])
    reviews_texts = [review["text"] for review in reviews]
    return reviews_texts


def get_token(code):
    url = "https://oauth2.googleapis.com/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "redirect_uri": "http://127.0.0.1:5000",  # One of the redirect URIs listed for your project in the API Console Credentials page for the given client_id. Not used but required.
    }
    response = requests.post(url, data=data)
    return response.json().get("refresh_token")


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
]
