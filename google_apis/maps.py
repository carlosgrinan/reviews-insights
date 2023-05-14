import googlemaps


import os


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
