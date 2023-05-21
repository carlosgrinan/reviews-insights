import base64
import re


def message_parts_recursion(parts):
    """
    Receives a list of ``MessageParts`` and returns the text body of the first
    ``MessagePart`` in the hierarchy that has a text/plain ``mimeType``
    """

    for part in parts:
        if part["mimeType"] == "text/plain":
            data = base64.urlsafe_b64decode(part["body"]["data"]).decode()
            return data
        elif "parts" in part:
            return message_parts_recursion(part["parts"])

    return None


def get_text(message):
    """
    Returns the text body of a ``Message``
    """

    # Note that "payload" itself is a MessagePart.
    text = message_parts_recursion([message["payload"]])
    text = re.sub(r"http\S+", "", text)  # Remove URLs
    return text if text else ""
