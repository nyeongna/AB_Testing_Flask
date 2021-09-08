import pymysql

sql_conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='gorhf123',
    db='blog_db',
    charset='utf8')

def conn_mysqldb():
    if not sql_conn.open:
        sql_conn.ping(reconnect=True)
    return sql_conn


