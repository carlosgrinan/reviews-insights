from api import GmailApi
from openai_api import summarize


def sync(source):
    if source.refresh_token:
        gmail = GmailApi(source.refresh_token)
        emails_text = gmail.get_emails()
        summary = summarize(emails_text, type_of_text="customer support emails")
        return summary
