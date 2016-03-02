from src.util import sql

from src.core import item

def create_item_from_db(_item):
	my_item = item.Item(_item['name'])
	my_item.set_dict(_item)
	my_item.set_category_id(_item['category_id'])
	my_item.set_id(_item['id'])
	my_item.set_creator_id(_item['creator_id'])
	my_item.set_category_name(_item['category_name'])
	my_item.set_description(_item['description'])

	return my_item

def map_items_to_dict(items):
	items_dict = []
	for _item in items:
		items_dict.append(create_item_from_db(_item))

	return items_dict

def get_latest_items():
	query = 'SELECT items.*, categories.name as category_name \
	FROM items \
	LEFT JOIN categories ON items.category_id = categories.id \
	ORDER BY id DESC LIMIT 20'

	items = sql.run_simple_sql_with_result(query, ())
	return map_items_to_dict(items)

def get_items_for(category):
	query = 'SELECT items.*, categories.name as category_name \
	FROM items \
	LEFT JOIN categories ON items.category_id = categories.id \
	WHERE items.category_id = (SELECT categories.id FROM categories WHERE categories.name = %s) ORDER BY name ASC'

	items = sql.run_simple_sql_with_result(query, (category, ))
	return map_items_to_dict(items)

def get_item(category_name, item_name):
	query = 'SELECT items.*, categories.name as category_name \
	FROM items \
	LEFT JOIN categories ON items.category_id = categories.id \
	WHERE category_id = (SELECT categories.id FROM categories WHERE categories.name = %s) AND items.name = %s'

	items = sql.run_simple_sql_with_result(query, (category_name, item_name))
	return map_items_to_dict(items)[0]

def get_item_by_id(category_id, item_id):
	query = 'SELECT items.*, categories.name as category_name \
	FROM items \
	LEFT JOIN categories ON items.category_id = categories.id \
	WHERE category_id = %s AND items.id = %s'

	items = sql.run_simple_sql_with_result(query, (category_id, item_id))
	return map_items_to_dict(items)[0]

def get_item_by_category_id_item_name(category_id, item_name):
	query = 'SELECT items.*, categories.name as category_name \
	FROM items \
	LEFT JOIN categories ON items.category_id = categories.id \
	WHERE category_id = %s AND items.name = %s'

	items = sql.run_simple_sql_with_result(query, (category_id, item_name))
	return map_items_to_dict(items)[0]

def delete_item(item_id):
	query = 'DELETE FROM items WHERE id = %s RETURNING *'

	deleted_item = sql.run_simple_sql_with_result(query, (item_id, ))
	return deleted_item[0]

def find_item(item_id):
	query = 'SELECT * FROM items WHERE id = %s'

	items = sql.run_simple_sql_with_result(query, (item_id, ))
	return map_items_to_dict(items)

def create_item(_item):
	query = 'INSERT INTO items (creator_id, category_id, name, description) VALUES (%s, %s, %s, %s) RETURNING *'

	new_item = sql.run_simple_sql_with_result(query, (_item.creator_id, _item.category_id, _item.name, _item.description))
	new_item = get_item_by_id(new_item[0]['category_id'], new_item[0]['id'])
	return new_item

def update_item(_item):
	query = 'UPDATE items SET category_id = %s, name = %s, description = %s WHERE id = %s RETURNING *'

	updated_item = sql.run_simple_sql_with_result(query, (_item.category_id, _item.name, _item.description, _item.id))
	updated_item = get_item_by_id(updated_item[0]['category_id'], updated_item[0]['id'])
	return updated_item

