def refresh_summary(source):
    from odoo.addons.proyecto_dam.openai_api import summarize

    from .api import BusinessProfile

    business_profile = BusinessProfile(source.refresh_token)
    reviews = business_profile.get_reviews()
    if reviews:
        summary = summarize(reviews, text_type="reviews")
        return summary
