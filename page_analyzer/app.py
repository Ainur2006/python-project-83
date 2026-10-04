import os

from dotenv import load_dotenv
from flask import (
    Flask, 
    render_template, 
    request, 
    flash,      
    redirect,
    url_for
    )
from .urls_repository import UrlsRepository
from .validator import validate_url


load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["DATABASE_URL"] = os.getenv("DATABASE_URL")

repo = UrlsRepository(app.config["DATABASE_URL"])


@app.get('/')
def index():
    return render_template('urls/index.html')


@app.get('/urls')
def urls_get():
    urls = repo.get_content()
    return render_template(
        'urls/show_urls.html',
        urls=urls,
        )


@app.post('/urls')
def urls_post():
    url = request.form.get('url', '').strip()
    errors = validate_url(url)
    if errors:
        return render_template(
            'urls/index.html',
            url=url,
            errors=errors,
        ), 422
    repo.save(url)
    flash('URL успешно добавлен!', 'success')
    return redirect(url_for('urls_get'))


@app.get('/urls/<id>')
def urls_show(id):
    url = repo.find(id)
    return render_template(
        'urls/show.html',
        url=url,
    )

