def refresh_summary(source):
    from odoo.addons.reviews_insights.openai_api import summarize

    from .api import PlayDeveloper

    play_developer = PlayDeveloper(source.refresh_token)
    package_name = source.config_id
    reviews = play_developer.get_reviews(package_name)
    if reviews:
        summary = summarize(reviews, text_type="app reviews from Google Play")
        return summary
