import validators


def validate_url(url):
    if not url:
        return "URL обязателен"
    if len(url) > 255:
        return "URL больше 255 символов!"
    if not validators.url(url):
        return "URL некорректный"
    return None