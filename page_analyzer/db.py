from psycopg2.extras import RealDictCursor, NamedTupleCursor

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
        column_name, value = list(search.items())[0]        
        sql = f'SELECT {str_cols} FROM {self.table_name} WHERE {column_name} = %s;'        
        with self.conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute(sql, (value, ))
            row = curs.fetchall()
        return row
    
    def select_element(self, element, search):
        column_name, value = list(search.items())[0]        
        sql = f'SELECT {element} FROM {self.table_name} WHERE {column_name} = %s;'        
        with self.conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute(sql, (value, ))
            result = curs.fetchone()
            if not result:
                return None
            return result[element]
    
    def insert(self, row, returning):
        columns_names = ', '.join(list(row.keys()))
        values = tuple(row.values())
        number_of_columns = ', '.join(['%s' for _ in range(len(values))])
        sql = f'''INSERT INTO {self.table_name} ({columns_names}) VALUES 
                 ({number_of_columns}) RETURNING {returning};'''
        with self.conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute(sql, values)
            element = curs.fetchone()[returning]
            self.conn.commit()
        return element