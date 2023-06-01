from googleapiclient.http import HttpMock

from odoo.addons.proyecto_dam.google_apis.api import GoogleApi

from .utils import get_text

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
]


class Gmail(GoogleApi):
    def __init__(self, refresh_token, mock=False):
        super().__init__(
            "gmail",
            "v1",
            refresh_token,
            mock=mock,
        )

    def get_emails(self, mock=False):
        """
        Returns a list consisting of the text body (string) of the 3 more recent emails in the user's inbox. Avoids forwarded and replied emails.
        """

        request = (
            self.service.users()
            .messages()
            .list(
                userId="me",
                labelIds=["INBOX"],
                maxResults=3,
                q="-is:forward -is:reply",  # exclude forwarded and replied emails because they contain the original email
                fields="messages/id",
            )
        )

        if mock:
            http_mock = HttpMock(
                "/home/carlos/src/odoo/addons/proyecto_dam/mock_data/google/gmail/messages-list.json", {"status": "200"}
            )
            response = request.execute(http=http_mock)
        else:
            response = request.execute()

        minimal_messages = response.get("messages", [])

        # LIST returns the messages in 'minimal' format (doesn't include the body)
        # Now we need to GET the
        # messages in 'full' format one by one (of course, the requests are batched):
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
        # if mock:
        #     http_batch_mock = ...
        #     messages = batch.execute(http=http_batch_mock)
        # else:
        messages = batch.execute()

        text_bodies = [get_text(message) for message in messages]
        text_bodies = [text_body for text_body in text_bodies if text_body]  # remove None values
        return text_bodies
