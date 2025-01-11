from psycopg2.extras import RealDictCursor

class Table:
    def __init__(self, conn, table_name):
        self.conn = conn
        self.table_name = table_name
    
    def select_all(self):
        sql = f'SELECT * FROM {self.table_name}'
        with self.conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute(sql)
            table = curs.fetchall()
        return table
    
    def select_row(self, columns, search):
        str_cols = ', '.join(columns)
        str_search = ' = '.join(list(search.items())[0])
        sql = f'SELECT {str_cols} FROM {self.table_name} WHERE {str_search};'
        with self.conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute(sql)
            row = curs.fetchall()
        return row
    
    def select_element(self, element, search):
        table_name, value = list(search.items())[0]
        
        query = f'SELECT {element} FROM {self.table_name} WHERE {table_name} = '
        
        sql = query + '%s;'
        with self.conn.cursor() as curs:
            curs.execute(sql, (value, ))
            element = curs.fetchone()[0]
        return element
    
    def insert(self, row):
        columns_names = ', '.join(list(row.keys()))
        values = ', '.join(list(row.values()))
        sql = f'INSERT INTO {self.table_name} ({columns_names}) VALUES ({values}) RETURNING url_id;'
        with self.conn.cursor() as curs:
            curs.execute(sql)
            self.conn.commit()
            url_id = curs.fetchone()[0]
        return url_id