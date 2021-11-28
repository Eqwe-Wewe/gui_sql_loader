from psycopg2 import connect as postgresql_connect, Error as postgresql_Error
from mysql.connector import connect as mysql_connect, Error as mysql_Error


class DataBaseError(Exception):
    pass


class DataBase:
    def __init__(self, config: dict, db_type):
        self.config = config
        self.db_type = db_type
    
    def __enter__(self):
        if self.db_type == 'MySQL':
            connect = mysql_connect
            Error = mysql_Error
        elif self.db_type == 'PostgresSQL':
            connect = postgresql_connect
            Error = postgresql_Error
        try:
            self.conn = connect(**self.config)
            self.cursor = self.conn.cursor()
            return self.cursor
        except Error as err:
            raise DataBaseError(err)
            self.conn.rollback()

    def __exit__(self, exc_type, exc_value, exc_trace):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        if exc_type:
            raise exc_type(exc_value)
