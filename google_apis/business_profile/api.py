from odoo.addons.proyecto_dam.google_apis.api import GoogleApi
from googleapiclient.http import HttpMock

SCOPES = [
    "https://www.googleapis.com/auth/business.manage",
]


class AccountManagement(GoogleApi):
    def __init__(self, refresh_token, mock=False):
        super().__init__(
            "mybusinessaccountmanagement",
            "v1",
            refresh_token,
            mock=mock,
            mock_file=None,
        )

    def get_accounts(self, mock=False):
        request = self.service.accounts().list(fields="accounts/name")

        if mock:
            http_mock = HttpMock("mock_data/google/business_profile/accounts-list.json", {"status": "200"})
            response = request.execute(http=http_mock)
        else:
            response = request.execute()

        accounts_ids = [account["name"].replace("accounts/", "") for account in response.get("accounts", [])]
        return accounts_ids


class BusinessInformation(GoogleApi):
    def __init__(self, refresh_token, mock=False):
        super().__init__(
            "mybusinessbusinessinformation",
            "v1",
            refresh_token,
            mock=mock,
        )

    def get_locations(self, account_id, mock=False):
        request = self.service.accounts().locations().list(parent=f"accounts/{account_id}", readMask="locations.name")

        if mock:
            http_mock = HttpMock("mock_data/google/business_profile/locations-list.json", {"status": "200"})
            response = request.execute(http=http_mock)
        else:
            response = request.execute()

        locations_ids = [
            location["name"].replace(f"accounts/{account_id}/locations/", "") for location in response.get("locations", [])
        ]
        return locations_ids


class MyBusiness(GoogleApi):
    def __init__(self, refresh_token, mock=False):
        super().__init__(
            "mybusiness",
            "v4",
            refresh_token,
            mock=mock,
            discoveryServiceUrl="https://developers.google.com/my-business/samples/mybusiness_google_rest_v4p9.json",
        )

    def get_reviews(self, account_id, location_id, mock=False):
        request = (
            self.service.accounts()
            .locations()
            .reviews()
            .list(parent=f"accounts/{account_id}/locations/{location_id}", fields="reviews/comment")
        )

        if mock:
            http_mock = HttpMock("mock_data/google/business_profile/reviews-list.json", {"status": "200"})
            response = request.execute(http=http_mock)
        else:
            response = request.execute()

        reviews = response.get("reviews", [])
        reviews_text = [review["comment"] for review in reviews]
        return reviews_text


class BusinessProfile:
    def __init__(self, refresh_token, mock=False):
        self.account_management = AccountManagement(refresh_token, mock=mock)
        self.business_information = BusinessInformation(refresh_token, mock=mock)
        self.my_business = MyBusiness(refresh_token, mock=mock)

    def get_reviews(self, mock=False):
        account = self.account_management.get_accounts(mock=mock)[0]
        location = self.business_information.get_locations(account, mock=mock)[0]
        reviews = self.my_business.get_reviews(account, location, mock=mock)
        return reviews
