import os
import datetime
import requests
from flask import (Flask, render_template, request, flash,
                   redirect, url_for, get_flashed_messages)
from dotenv import load_dotenv
from .db import DataBase
from .utils import normalize_url, get_info, validate_url


app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')


@app.get('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def post_new_url():
    url = request.form.get('url')
    error = validate_url(url)
    if error:
        flash(error, 'danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html', messages=messages), 422
    normalized_url = normalize_url(url)
    date = datetime.date.today()
    connection = DataBase(app)
    id = connection.select_id_from_urls(normalized_url)
    if id:
        flash('Страница уже существует', 'primary')
        return redirect(url_for('get_url_info', id=id))
    id = connection.insert_in_urls(normalized_url, date)
    flash('Страница успешно добавлена', 'success')
    connection.close_connection()
    return redirect(url_for('get_url_info', id=id))


@app.route('/urls/<id>')
def get_url_info(id):
    connection = DataBase(app)
    url = connection.select_row_from_urls(id)
    checks = connection.select_row_from_url_checks(id)
    messages = get_flashed_messages(with_categories=True)
    connection.close_connection()
    return render_template('url.html',
                           url=url,
                           messages=messages,
                           checks=checks,
                           id=id)


@app.route('/urls')
def get_all_urls():
    connection = DataBase(app)
    urls = connection.select_urls_with_last_check()
    connection.close_connection()
    return render_template('urls.html', urls=urls)


@app.post('/urls/<id>/checks')
def post_checks(id):
    connection = DataBase(app)
    url = connection.select_row_from_urls(id).name
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        connection.close_connection()
        return redirect(url_for('get_url_info', id=id))
    date = str(datetime.date.today())
    url_info = get_info(response)
    url_info['url_id'] = id
    url_info['created_at'] = date
    flash('Страница успешно проверена', 'success')
    connection.insert_into_url_checks(url_info)
    connection.close_connection()
    return redirect(url_for('get_url_info', id=id))
