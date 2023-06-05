from googleapiclient.http import HttpMock

from odoo.addons.reviews_insights.google_apis.api import GoogleApi

SCOPES = [
    "https://www.googleapis.com/auth/androidpublisher",
]


class PlayDeveloper(GoogleApi):
    def __init__(self, refresh_token, mock=False):
        super().__init__(
            "androidpublisher",
            "v3",
            refresh_token,
            mock=mock,
        )

    def get_reviews(self, package_name, mock=False):
        """
        There is no way to obtain package names of apps associated with the account, so te user must provide it.
        """
        request = self.service.reviews().list(
            packageName=package_name,
            maxResults=10,
            translationLanguage="en",
            fields="reviews/comments/userComment/text",
        )

        if mock:
            http_mock = HttpMock(
                "/home/carlos/src/odoo/addons/reviews_insights/mock_data/google/play_developer/reviews-list.json",
                {"status": "200"},
            )
            response = request.execute(http=http_mock)
        else:
            response = request.execute()

        reviews = response.get("reviews", [])
        reviews_text = [review["comments"][0]["userComment"]["text"] for review in reviews]
        return reviews_text
