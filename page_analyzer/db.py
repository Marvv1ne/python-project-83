import psycopg2
from psycopg2.extras import RealDictCursor



#conn = psycopg2.connect(DATABASE_URL)


class UrlsTable:
    def __init__(self, conn):
        self.conn = conn
    
    def insert(self, name, created_at):
        sql = "INSERT INTO urls (name, created_at) VALUES (%(name)s, %(created_at)s) ON CONFLICT (name) DO NOTHING;"
        with self.conn.cursor() as curs:
            curs.execute(sql, {'name': name, 'created_at': created_at})
            self.conn.commit()
            id = self._get_id(name)
        return id
    
    def _get_id(self, name):
        sql = "SELECT id FROM urls WHERE name=%(name)s;"
        with self.conn.cursor() as curs:
            curs.execute(sql, {'name': name})
            id = curs.fetchone()[0]
        return id

    def get_row(self, id):
        sql = "SELECT * FROM urls WHERE id=%(id)s;"
        with self.conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute(sql, {'id': id})
            row = curs.fetchone()
        return row
    
    def get_all(self):
        sql = "SELECT * FROM urls;"
        with self.conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute(sql)
            table = curs.fetchall()
        return table
    