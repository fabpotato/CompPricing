import psycopg2
from contextlib import contextmanager

@contextmanager
def connect_db(host, db_name, user, password):
    conn = psycopg2.connect(
        host=host,
        dbname=db_name,
        user=user,
        password=password)
    yield conn
    conn.close()

