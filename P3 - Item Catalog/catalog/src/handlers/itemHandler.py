from src.core import item
from src.dao import itemsDAO
from src.handlers import userHandler

# handler used for convenience

# create item from an request object, form post
def item_from_request(request):
	my_item = item.Item(request.form['name'])
	my_item.set_category_id(request.form['category_id'])
	my_item.set_description(request.form['description'])
	my_item.set_id(request.form['id'])
	my_item.set_creator_id(request.form['creator_id'])
	return my_item

def create_item(my_item):
	new_item = itemsDAO.create_item(my_item)
	return new_item

def update_item(my_item):
	updated_item = itemsDAO.update_item(my_item)
	return updated_item

def delete_item(my_item):
	deleted_item = itemsDAO.delete_item(my_item.id)
	return deleted_item