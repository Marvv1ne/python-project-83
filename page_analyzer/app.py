import os
import psycopg2
from psycopg2.extras import RealDictCursor
import validators
import datetime
from flask import Flask, render_template, request, flash, redirect, url_for, get_flashed_messages
from dotenv import load_dotenv
from urllib.parse import urlparse
from .db import DataBase
from .url_parser import get_info



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
    req = DataBase(conn=conn)
    id = req.select_id_from_urls(normalized_url)
    if id:
        flash('Страница уже существует', 'primary')
        return redirect(url_for('get_new', id=id))
    id = req.insert_in_urls(normalized_url, date)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_new', id=id))

@app.route('/urls/<id>')
def get_new(id):
    req = DataBase(conn=conn)
    url = req.select_row_from_urls(id)
    infos = req.select_row_from_url_checks(id)
    messages = get_flashed_messages(with_categories=True)
    return render_template('url.html', url=url, messages=messages, infos=infos, id=id)

@app.route('/urls')
def get_all():
    req = DataBase(conn=conn)
    urls = req.select_all_from_urls()
    return render_template('urls.html', urls=urls)

@app.post('/urls/<id>/checks')
def post_checks(id):
    req = DataBase(conn=conn)
    url = req.select_row_from_urls(id).name
    
    date = str(datetime.date.today())
    url_info = get_info(url)
    url_info['url_id'] = id
    url_info['created_at'] = date
    req.insert_into_url_checks(url_info)
    
    return redirect(url_for('get_new', id=id))


    

    

if __name__ == '__main__':
    app.run()