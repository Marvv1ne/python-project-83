import os
import psycopg2
from psycopg2.extras import RealDictCursor
import validators
import datetime
from flask import Flask, render_template, request, flash, redirect, url_for, get_flashed_messages
from dotenv import load_dotenv
from urllib.parse import urlparse
from .db import Table



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
    req = Table(conn=conn, table_name='urls')
    id = req.select_element('id', {'name': normalized_url})
    if id:
        flash('Страница уже существует', 'primary')
        return redirect(url_for('get_new', id=id))
    id = req.insert({'name': normalized_url, 'created_at': date}, returning='id')
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_new', id=id))

@app.route('/urls/<id>')
def get_new(id):
    req_urls = Table(conn=conn, table_name='urls')
    req_checks = Table(conn=conn, table_name='url_checks')
    url = req_urls.select_row('*', {'id': id})[0]
    infos = req_checks.select_row('*', {'url_id':id})
    messages = get_flashed_messages(with_categories=True)
    return render_template('url.html', url=url, messages=messages, infos=infos, id=id)

@app.route('/urls')
def get_all():
    req = Table(conn=conn, table_name='urls')
    urls = req.select_all()
    return render_template('urls.html', urls=urls)

@app.post('/urls/<id>/checks')
def post_checks(id):
    req = Table(conn=conn, table_name='url_checks')
    date = str(datetime.date.today())
    values = {'url_id': id, 'created_at': date}
    element = req.insert(values, returning='url_id')
    return redirect(url_for('get_new', id=element))


    

    

if __name__ == '__main__':
    app.run()