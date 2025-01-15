from psycopg2.extras import RealDictCursor, NamedTupleCursor

class DataBase:
    def __init__(self, conn):
        self.conn = conn
    
    def insert_in_urls(self, name, created_at):
        sql = 'INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id;'
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(sql, (name, created_at))
            self.conn.commit()
            return curs.fetchone().id
    
    def insert_into_url_checks(self, url_info):
        sql = '''INSERT INTO url_checks (url_id, status_code, h1,
                                       title, description, created_at)
                VALUES (%(url_id)s, %(status_code)s, %(h1)s, %(title)s, %(description)s, %(created_at)s)'''
        #url_info['url_id'] = url_id
        #url_info['created_at'] = created_at
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(sql, url_info)
            self.conn.commit()
                    
    def select_all_from_urls(self):
        sql = f'SELECT * FROM urls'
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
        sql = 'SELECT * FROM url_checks WHERE url_id=%s;'
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(sql, (url_id,))
            return curs.fetchall()
    
