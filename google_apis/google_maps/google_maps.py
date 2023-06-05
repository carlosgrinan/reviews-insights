import googlemaps
import os
from dotenv import load_dotenv
from googlemaps.exceptions import ApiError


def get_reviews(place_id):
    load_dotenv()
    gmaps = googlemaps.Client(key=os.getenv("GOOGLE_API_KEY"))
    try:
        response = gmaps.place(
            place_id,
            fields=["reviews"],
            language="en",
            reviews_sort="most_relevant",
        )
    except ApiError as e:
        print(e.message)
        return []
    reviews = response["result"].get("reviews", [])
    reviews_texts = [review["text"] for review in reviews]
    return reviews_texts
