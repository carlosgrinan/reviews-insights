def sync(source):
    from odoo.addons.proyecto_dam.openai_api import summarize
    from .api import Gmail

    if source.refresh_token:
        gmail = Gmail(source.refresh_token)
        emails_text = gmail.get_emails()
        summary = summarize(emails_text, type_of_text="customer support emails")
        return summary
