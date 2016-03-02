import hashlib
import uuid
# import os can be used for salt, but gave error. not sure why yet

from src.dao import userDAO
from src.core import user

def get_hashed_password(password, salt):
	return hashlib.sha256(salt.encode() + password.encode()).hexdigest()

def confirm_password(username, password):
	salt = userDAO.get_user_salt(username)
	return userDAO.get_user_password(username) == get_hashed_password(password, salt)

def confirm_user_creds(username, password):
	user = userDAO.find_user(username) 
	if user and confirm_password(username, password):
		return user
	return None

def login_user(username, password):
	return confirm_user_creds(username, password)

def register_user(my_user):
	# salt = os.urandom(18) #gives decode error
	salt = uuid.uuid4().hex
	my_user.set_salt(salt)
	my_user.set_password(get_hashed_password(my_user.password, salt))
	return userDAO.create_user(my_user)

def register_user_oauth(my_user):
	# salt = os.urandom(18) #gives decode error
	return userDAO.create_user_oauth(my_user)

def get_user(username):
	return userDAO.find_user(username)