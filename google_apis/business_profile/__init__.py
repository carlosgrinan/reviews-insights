def refresh_summary(source):
    from odoo.addons.reviews_insights.openai_api import summarize, translate

    from .api import BusinessProfile

    business_profile = BusinessProfile(source.refresh_token, mock=True)
    # Mocking reviews until Google grants us cuota for the 3 APIs and access to My Business API (which is not going to happen because we are not a real business)
    reviews = business_profile.get_reviews(mock=True)
    if reviews:
        translation = translate(reviews)
        if translation:
            summary = summarize(translation, text_type="reviews")
            return summary
