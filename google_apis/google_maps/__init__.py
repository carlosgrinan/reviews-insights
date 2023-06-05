def refresh_summary(source):
    from odoo.addons.reviews_insights.openai_api import summarize

    from . import google_maps

    place_id = source.config_id
    reviews = google_maps.get_reviews(place_id)
    if reviews:
        summary = summarize(reviews, text_type="reviews")
        return summary
