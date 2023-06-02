def refresh_summary(source):
    from odoo.addons.reviews_insights.openai_api import summarize

    from .api import Gmail

    gmail = Gmail(source.refresh_token)
    emails = gmail.get_emails()
    if emails:
        summary = summarize(emails, text_type="customer support emails")
        return summary
