import pymysql
import os

def create_conn():
    conn = pymysql.connect(host='localhost',
            user=os.environ['mysql_username'],
            password=os.environ['mysql_pass'],
            db='VenmoDB',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)
    c = conn.cursor()
    return conn, c

def close_conn(conn, cur):
    cur.close()
    conn.close()