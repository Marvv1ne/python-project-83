import psycopg2
from psycopg2.extras import NamedTupleCursor


def connect_to_db(app):
    return psycopg2.connect(app.config['DATABASE_URL'])


class DataBase:
    def __init__(self, conn):
        self.conn = conn

    def insert_in_urls(self, name, created_at):
        sql = '''INSERT INTO urls (name, created_at)
                 VALUES (%s, %s) RETURNING id;'''
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            try:
                curs.execute(sql, (name, created_at))
                self.conn.commit()
                return curs.fetchone().id
            except Exception as e:
                self.conn.rollback()
                raise e

    def insert_into_url_checks(self, url_info):
        sql = '''INSERT INTO url_checks (url_id, status_code, h1,
                                       title, description, created_at)
                VALUES (%(url_id)s, %(status_code)s, %(h1)s,
                        %(title)s, %(description)s, %(created_at)s)'''
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            try:
                curs.execute(sql, url_info)
                self.conn.commit()
            except Exception as e:
                self.conn.rollback()
                raise e

    def select_all_from_urls(self):
        sql = 'SELECT * FROM urls ORDER BY id DESC'
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(sql)
            table = curs.fetchall()
        return table

    def select_row_from_urls(self, id):
        sql = 'SELECT * FROM urls WHERE id=%s;'
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(sql, (id, ))
            row = curs.fetchone()
        return row

    def select_id_from_urls(self, name):
        sql = 'SELECT id FROM urls WHERE name=%s;'
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(sql, (name, ))
            result = curs.fetchone()
            if result is None:
                return None
            return result.id

    def select_row_from_url_checks(self, url_id):
        sql = 'SELECT * FROM url_checks WHERE url_id=%s ORDER BY id DESC;'
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(sql, (url_id,))
            return curs.fetchall()

    def select_urls_with_last_check(self):
        sql = '''SELECT urls.id as id,
                        urls.name as name,
                        url_checks.created_at as last_check,
                        url_checks.status_code as response_code
                FROM urls
                LEFT JOIN url_checks ON urls.id = url_checks.url_id
                ORDER BY urls.id DESC;
            '''
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(sql)
            return curs.fetchall()
