import os
import psycopg2
from psycopg2.extras import RealDictCursor
import validators
import datetime
from flask import Flask, render_template, request, flash, redirect, url_for
from dotenv import load_dotenv
from urllib.parse import urlparse


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
        flash('Wrong url!')
        return render_template('index.html')
    normalized_url = f'{urlparse(url).scheme}://{urlparse(url).netloc}'
    date = datetime.date.today()
    with conn.cursor() as curs:
        curs.execute('INSERT INTO urls (name, created_at) VALUES (%(name)s, %(created_at)s) ON CONFLICT ("name") DO UPDATE SET "name" = %(name)s RETURNING id;', {"name": normalized_url, "created_at": date})
        id = curs.fetchone()[0]
    conn.commit()
    return redirect(url_for('get_new', id=id))

@app.route('/urls/<id>')
def get_new(id):
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute('SELECT * FROM urls WHERE id=%(id)s', {'id': id})
        return curs.fetchone()

@app.route('/urls')
def get_all():
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute('SELECT * FROM urls')
        return curs.fetchall()


    

    

if __name__ == '__main__':
    app.run()
