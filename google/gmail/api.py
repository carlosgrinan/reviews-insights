from google.api import GoogleApi
from google.gmail.utils import get_text


from googleapiclient.http import HttpMock


from pprint import pprint


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


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
]
