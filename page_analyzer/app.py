import os
import psycopg2
from psycopg2.extras import RealDictCursor
import validators
import datetime
from flask import Flask, render_template, request, flash, redirect, url_for, get_flashed_messages
from dotenv import load_dotenv
from urllib.parse import urlparse
from .db import UrlsTable


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')

conn = psycopg2.connect(DATABASE_URL)


@app.get('/')
def index():
    return render_template('index.html')

@app.post('/')
def post_new():
    url = request.form.get('url')
    if not validators.url(url):
        flash('Некорректный URL', 'error')
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html', messages)
    normalized_url = f'{urlparse(url).scheme}://{urlparse(url).netloc}'
    date = datetime.date.today()
    req = UrlsTable(conn)
    id = req.get_id(name=normalized_url)
    if id:
        flash('Страница уже существует', 'primary')
        return redirect(url_for('get_new', id=id))
    id = req.insert(name=normalized_url, created_at=date)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_new', id=id))

@app.route('/urls/<id>')
def get_new(id):
    req = UrlsTable(conn)
    url = req.get_row(id)
    messages = get_flashed_messages(with_categories=True)
    return render_template('url.html', url=url, messages=messages)

@app.route('/urls')
def get_all():
    req = UrlsTable(conn)
    urls = req.get_all()
    return render_template('urls.html', urls=urls)


    

    

if __name__ == '__main__':
    app.run()
