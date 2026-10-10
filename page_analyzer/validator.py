import validators
from urllib.parse import urlparse


def validate_url(url):
    if not url:
        return "URL обязателен"
    if len(url) > 255:
        return "URL больше 255 символов!"
    if not validators.url(url):
        return "URL некорректный"
    return None

def normalize_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme.lower()}://{parsed_url.netloc.lower()}"