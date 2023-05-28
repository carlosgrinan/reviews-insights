def refresh_summary(source):
    from odoo.addons.proyecto_dam.openai_api import summarize

    from . import google_maps

    reviews = google_maps.get_reviews(source.place_id)
    if reviews:
        summary = summarize(reviews, text_type="reviews")
        return summary
