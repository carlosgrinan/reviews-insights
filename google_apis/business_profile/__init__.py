def refresh_summary(source):
    from odoo.addons.reviews_insights.openai_api import summarize, translate

    from .api import BusinessProfile

    business_profile = BusinessProfile(
        source.refresh_token,
    )
    reviews = business_profile.get_reviews()
    if reviews:
        translation = translate(reviews)
        summary = summarize(translation, text_type="reviews")
        return summary
