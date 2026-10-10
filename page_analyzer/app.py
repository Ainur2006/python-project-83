import os

import requests
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from .parser import parse_html
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
    urls = repo.get_last_check()
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
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('urls_get'))


@app.get('/urls/<id>')
def urls_show(id):
    url = repo.find(id)
    checks = repo.get_content_checks(id)
    return render_template(
        'urls/show.html',
        url=url,
        checks=checks,
    )


@app.post('/urls/<id>/checks')
def url_check_post(id):
    url_data = repo.find(id)
    try:
        response = requests.get(url_data['name'])
        response.raise_for_status()
    except requests.RequestException as e:
        app.logger.info(e)
        flash('Произошла ошибка при проверке', 'error')
        return redirect(url_for('urls_show', id=id))

    url_check_data = parse_html(url_data['name'])
    repo.save_checks(id, url_check_data)
    app.logger.info("Saving check for url_id=%s", id)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('urls_show', id=id))