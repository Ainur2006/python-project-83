import requests
from bs4 import BeautifulSoup

def truncate(text):
    if text is None:
        return None
    if len(text) <= 255:
        return text
    return text[:252] + '...'

def parse_html(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    
    h1 = soup.find("h1")
    title = soup.find("title")
    meta = soup.find("meta", attrs={"name": "description"})
    return {
        'status_code': response.status_code,
        'h1': truncate(h1.get_text(strip=True)[:255]) if h1 else None,
        'title': truncate(title.get_text(strip=True)[:255]) if title else None,
        'description': truncate(meta.get('content')[:255]) if meta else None, 
    }