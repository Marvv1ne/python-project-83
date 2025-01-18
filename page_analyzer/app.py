import os
import datetime
import requests
from flask import (Flask, render_template, request, flash,
                   redirect, url_for, get_flashed_messages)

from .db import DataBase, connect_to_db
from .url_parser import normalize_url, get_info, validate_url

try:
    from dotenv import load_dotenv
    load_dotenv()
except ModuleNotFoundError:
    pass

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')


@app.get('/')
def index():
    return render_template('index.html')


@app.post('/')
def post_new():
    conn = connect_to_db(app)
    url = request.form.get('url')
    error = validate_url(url)
    if error:
        flash(error, 'danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html', messages=messages)
    normalized_url = normalize_url(url)
    date = datetime.date.today()
    req = DataBase(conn=conn)
    id = req.select_id_from_urls(normalized_url)
    if id:
        flash('Страница уже существует', 'primary')
        return redirect(url_for('get_new', id=id))
    id = req.insert_in_urls(normalized_url, date)
    flash('Страница успешно добавлена', 'success')
    conn.close()
    return redirect(url_for('get_new', id=id))


@app.route('/urls/<id>')
def get_new(id):
    conn = connect_to_db(app)
    req = DataBase(conn=conn)
    url = req.select_row_from_urls(id)
    infos = req.select_row_from_url_checks(id)
    messages = get_flashed_messages(with_categories=True)
    conn.close()
    return render_template('url.html',
                           url=url,
                           messages=messages,
                           infos=infos,
                           id=id)


@app.route('/urls')
def get_all():
    conn = connect_to_db(app)
    req = DataBase(conn=conn)
    urls = req.select_all_from_urls()
    conn.close()
    return render_template('urls.html', urls=urls)


@app.post('/urls/<id>/checks')
def post_checks(id):
    conn = connect_to_db(app)
    req = DataBase(conn=conn)
    url = req.select_row_from_urls(id).name
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        conn.close()
        return redirect(url_for('get_new', id=id))
    date = str(datetime.date.today())
    url_info = get_info(url)
    url_info['url_id'] = id
    url_info['created_at'] = date
    req.insert_into_url_checks(url_info)
    conn.close()
    return redirect(url_for('get_new', id=id))
