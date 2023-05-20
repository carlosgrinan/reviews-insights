from odoo.addons.proyecto_dam.openai_api import summarize
from . import google_maps


def sync(source):
    if source.place_id:
        reviews_texts = google_maps.get_reviews(source.place_id)
        summary = summarize(reviews_texts, type_of_text="reviews")
        return summary
