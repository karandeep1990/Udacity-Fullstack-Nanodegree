import psycopg2
import psycopg2.extras

def connect():
	return psycopg2.connect("dbname=catalog")

def run_simple_sql_with_result(sql, params):
	conn = connect()
	c = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	c.execute(sql, params)
	result = c.fetchall()
	conn.commit()
	conn.close()
	return result

def run_simple_sql_no_result(sql, params):
	conn = connect()
	c = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	c.execute(sql, params)
	conn.commit()
	conn.close()