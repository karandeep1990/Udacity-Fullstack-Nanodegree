from src.util import sql

from src.core import user

def create_user_from_db(_user):
	my_user = user.User(_user['name'])
	my_user.set_id(_user['id'])
	my_user.set_salt(_user['salt'])
	my_user.set_username(_user['username'])
	my_user.set_password(_user['pass'])
	my_user.set_social_id(_user['social_id'])

	return my_user

def map_items_to_dict(users):
	users_dict = []
	for _item in users:
		users_dict.append(create_user_from_db(_item))

	return users_dict

def find_user(username):
	query = 'SELECT * FROM users WHERE username = %s'

	user = sql.run_simple_sql_with_result(query, (username, ))
	user = map_items_to_dict(user)
	if (len(user) > 0):
		return user[0]
	else:
		return None

def get_user_salt(username):
	query = 'SELECT salt FROM users WHERE username = %s'

	salt = sql.run_simple_sql_with_result(query, (username, ))
	return salt[0][0]

def get_user_password(username):
	query = 'SELECT pass FROM users WHERE username = %s'

	pwd = sql.run_simple_sql_with_result(query, (username, ))
	return pwd[0][0]

def create_user(user):
	query = 'INSERT INTO users (name, username, salt, pass) VALUES (%s, %s, %s, %s) RETURNING *'
	user = sql.run_simple_sql_with_result(query, (user.name, user.username, user.salt, user.password))
	return map_items_to_dict(user)[0]

def create_user_oauth(user):
	query = 'INSERT INTO users (name, username, social_id) VALUES (%s, %s, %s) RETURNING *'
	user = sql.run_simple_sql_with_result(query, (user.name, user.username, user.username))
	return map_items_to_dict(user)[0]