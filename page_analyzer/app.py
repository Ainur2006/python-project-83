import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

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
    flash('URL успешно добавлен!', 'success')
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
    # url_data = repo.find(id)
    # try:
    #     pass
    # except:
    #     flash('Произошла ошибка при проверке', 'danger')
    #     return redirect(url_for('urls_show', id=id))
    app.logger.info("Saving check for url_id=%s", id)
    repo.save_checks(id)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('urls_show', id=id))