import requests
from bs4 import BeautifulSoup


def parse_html(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    
    h1 = soup.find("h1")
    title = soup.find("title")
    meta = soup.find("meta", attrs={"name": "description"})
    return {
        'status_code': response.status_code,
        'h1': h1.get_text(strip=True)[:255] if h1 else None,
        'title': title.get_text(strip=True)[:255] if title else None,
        'description': meta.get('content')[:255] if meta else None, 
    }