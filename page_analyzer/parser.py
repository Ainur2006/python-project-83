from bs4 import BeautifulSoup


def truncate(text):
    if text is None:
        return None
    if len(text) > 255:
        return text[:252] + '...'
    return text


def parse_html(html, status_code):
    soup = BeautifulSoup(html, 'html.parser')
    
    h1 = soup.find("h1")
    title = soup.find("title")
    meta = soup.find("meta", attrs={"name": "description"})

    return {
        'status_code': status_code,
        'h1': truncate(h1.get_text(strip=True)) if h1 else None,
        'title': truncate(title.get_text(strip=True)) if title else None,
        'description': truncate(meta.get('content')) if meta else None, 
    }