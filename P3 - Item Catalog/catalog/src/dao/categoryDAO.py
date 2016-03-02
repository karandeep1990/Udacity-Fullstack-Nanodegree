from src.util import sql

def get_all_categories():
	query = 'SELECT * FROM categories'

	categories = sql.run_simple_sql_with_result(query, ())

	categories_arr = []
	for category in categories:
		categories_arr.append({"id": category[0], "name": category[1]})
	
	return categories_arr