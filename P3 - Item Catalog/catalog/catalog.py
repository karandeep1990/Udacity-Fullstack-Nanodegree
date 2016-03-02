from flask import Flask, request, session, redirect, url_for, render_template, make_response, flash

app = Flask(__name__)

import os, traceback, json

from src.api import delegate
from src.handlers import userHandler
from src.handlers import categoryHandler
from src.handlers import itemHandler
from src.dao import categoryDAO
from src.dao import itemsDAO
from src.core import user
from src.core import item

# init the OAuth API
from src.api.oauth import OAuthService
OAuthService.init(app)


# home page, index.html, show latest items
@app.route('/')
def index(error = None):
	app.logger.debug("get latest items/ home")
	categories = None
	latest_items = None
	
	try:
		categories = categoryDAO.get_all_categories()
	except:
		error = " could not get categories"	
	
	latest_items = itemsDAO.get_latest_items()

	return render_template('index.html', categories = categories, items = latest_items, latest_items = True, error = error)

# items for the category (same page as home but specific items)
@app.route('/catalog/<category_name>/items')
def route_category(category_name, error = None):
	app.logger.debug("get itesm for category")
	categories = None
	category_items = None

	try:
		categories = categoryDAO.get_all_categories()
	except:
		error += " could not get categories"	

	category_items = itemsDAO.get_items_for(category_name)

	return render_template('index.html', categories = categories, selected_category = category_name, items = category_items, error = error)

# view the item
@app.route('/catalog/<category_name>/<item_name>')
def route_category_item(category_name, item_name, edit = False, error = None):
	app.logger.debug("get item route")
	
	categories = None
	category_item = None

	if error is None:
		error = ""

	try:
		categories = categoryDAO.get_all_categories()
	except:
		error += "could not get categories"	
	try:
		category_item = itemsDAO.get_item(category_name, item_name)
	except:
		error += "Could not get the Category Item"

	if 'user_id' in session and category_item.creator_id and category_item.creator_id == session['user_id']:
		edit = True


	if error == "":
		error = None
	return render_template('item.html', categories = categories, item = category_item, edit = edit, error = error)

# edit, delete or create an item
# note this is weird because item is not filtered by category in the url.. can be confusing
# as it may look like your deleting an item from the wrong category, 
# also meaning the items must be uniquly named now

@app.route('/catalog/new', methods=['GET', 'POST'])
def route_new_item():
	app.logger.debug("item new route")
	categories = categoryDAO.get_all_categories()
	error = None
	edit = False

	if 'logged_in' not in session:
		return redirect(url_for('route_login', error = 'Log in First'))

	if request.method == 'POST':
		category_item = None
		try:
			category_item = itemsDAO.get_item_by_category_id_item_name(request.form['category_id'], request.form['name'])	
		except:
			pass

		if category_item is not None:
			error = "item already exists"
			return redirect(url_for('route_category_item', category_name = category_item.category_name, item_name = category_item.name, error = error))

		new_item = None
		my_item = item.Item(request.form['name'])
		my_item.set_category_id(request.form['category_id'])
		my_item.set_description(request.form['description'])
		my_item.set_creator_id(session['user_id'])
		try:
			new_item = itemHandler.create_item(my_item)
		except Exception as inst:
			error = 'could not create item'
			app.logger.debug(inst)			
		if new_item is not None:
			return route_to_item(new_item, edit = False, error = error)
		
	return render_template('new_item.html', categories = categories, error = error)

# show edit page on get, edit the item on post and take back to item, if fail show edit page
@app.route('/catalog/<item_name>/edit', methods=['POST'])
def route_edit_item(item_name):
	app.logger.debug("item edit route")
	categories = categoryDAO.get_all_categories()
	error = None

	# kick it if not logged in
	if 'logged_in' not in session:
		error = "Log in First"
		return redirect(url_for('route_login', error = error))

	# override request method since you can come from items page (fake GET), not the edit page
	# only because we are not using the real GET, and since we are not allowing category in url
	request_method = "POST"
	if 'requestType' in request.form and request.form['requestType'] == "GET":
		request_method = "GET"

	# came directly through url, try kicking it back to edit page
	my_item = None
	try:
		my_item = itemsDAO.get_item_by_id(request.form['orig_category_id'], request.form['id']) 
	except Exception as inst:
		error = 'please come through item page'
		app.logger.debug(traceback.print_exc())
		return render_template('edit_item.html', categories = categories, item = my_item, error = error)

	# kick if not creator
	if 'user_id' in session and session['user_id'] != int(my_item.creator_id):
		error = 'not allowed to edit, only the creator can'
		app.logger.debug("not the item creator, thus cannot edit")
		return route_to_item(my_item, error = error)

	if request_method == 'POST':
		# try and update item, requires full item
		updated_item = None
		try:
			updated_item = itemHandler.update_item(itemHandler.item_from_request(request))
		except Exception as inst:
			app.logger.debug(traceback.print_exc())
			error = "count not update item"
		if updated_item is not None:
			app.logger.debug("updated Item, routing to item now")
			return route_to_item(updated_item, error = error)

	# show edit page on get
	return render_template('edit_item.html', categories = categories, item = my_item, error = error)

# delete item and go to home page if deleted, if fail go back to edit page
@app.route('/catalog/<item_name>/delete', methods=['POST'])
def route_delete_item(item_name):
	app.logger.debug("item delete route")
	categories = categoryDAO.get_all_categories()
	error = None
	edit = False

	# kick it when not logged in
	if 'logged_in' not in session:
		error = "log in first"
		return redirect(url_for('route_login', error = error))

	# override request method since you can come from items page (fake GET), not the edit page
	# only because we are not using the real GET, and since we are not allowing category in url
	request_method = "POST"
	if 'requestType' in request.form and request.form['requestType'] == "GET":
		request_method = "GET"

	# check if came through post, try kicking it back to edit page
	my_item = None
	try:
		my_item = itemsDAO.get_item_by_id(request.form['category_id'], request.form['id']) 
	except Exception as inst:
		error = 'please come through item page'
		app.logger.debug(traceback.print_exc())
		return render_template('edit_item.html', categories = categories, item = my_item, error = error)

	# kick if not creator
	if 'user_id' in session and session['user_id'] != int(my_item.creator_id):
		error = 'not allowed to edit'
		return route_to_item(my_item, error = error)
	
	if request_method == 'POST':
		# try delete item from form pose, required full item	
		deleted_item = None
		try:
			deleted_item = itemHandler.delete_item(my_item)
		except Exception as inst:
			error = 'coult not delete item'
			app.logger.debug(inst)
		if deleted_item is not None:
			app.logger.debug("deleted Item, routing to index now")
			return redirect(url_for('index'))

	# show delete page on get
	return render_template('delete.html', categories = categories, item = my_item, error = error)


def route_to_item(my_item, edit = False, error = None):
	category = my_item.category_name
	name = my_item.name
	description = my_item.description
	return redirect(url_for('route_category_item', category_name = category, item_name = name, edit = edit, error = error))

# show login page on GET, log use in on post
@app.route('/login', methods=['GET', 'POST'])
def route_login(error = None):
	# handle POST
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		user = userHandler.login_user(username, password)
		if user and user.id:
			session['username'] = user.username
			session['user_id'] = user.id
			session['logged_in'] = True
			return redirect(url_for('index'))
		else:
			error = 'invalid username or password'
	
	# handle GET or error
	return render_template('login.html', error = error)


# login using provider via redirect
@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if 'logged_in' in session:
        return redirect(url_for('index'))
    oauth = OAuthService.OAuthSignIn.get_provider(provider)
    return oauth.authorize()

# redirect after user logs in via provider
@app.route('/callback/<provider>')
def oauth_callback(provider):
    if 'logged_in' in session:
        return redirect(url_for('index'))

    oauth = OAuthService.OAuthSignIn.get_provider(provider)
    try:
    	social_id, name = oauth.callback()
    except Exception as inst:
    	app.logger.debug(traceback.print_exc())
    	error = "auth failed"
        flash("could not get proper login response")
        return redirect(url_for('route_login', error = error))

    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    
    # get user, else create one using social id
    app.logger.debug(social_id)

    logged_user = userHandler.get_user(social_id)

    #register user
    if logged_user is None:
		my_user = user.User(name)
		my_user.set_username(social_id)
        
		logged_user = userHandler.register_user_oauth(my_user)
		if logged_user is None:
			flash("Registration failed")
			return redirect(url_for('route_login'))

    # add to session
    session['username'] = logged_user.username
    session['logged_in'] = True
    session['user_id'] = logged_user.id
    return redirect(url_for('index'))

# log out the user

@app.route('/logout')
def route_logout():
	session.pop('username', None)
	session.pop('logged_in', None)
	session.pop('user_id', None)
	return redirect(url_for('index'))

# add user route
@app.route('/register', methods=['GET', 'POST'])
def route_register_user():
	error = None
	if request.method == 'POST':
		my_user = user.User(request.form['name'])
		my_user.set_username(request.form['username'])
		my_user.set_password(request.form['password'])

		if userHandler.register_user(my_user):
			return redirect(url_for('route_login'))
		else:
			error = 'Count not create a user'
	# handle GET or error
	return render_template('register.html', error = error)

@app.route('/catalog.<fmt>')
def api_delegate(fmt = 'json'):
	app.logger.debug('Delegate API request')
	#delegate.delegate_request(request)

	categories = categoryDAO.get_all_categories()

	cat_json = {'category':[]}
	for category in categories:
		category_items = itemsDAO.get_items_for(category['name'])
		cat_items_dict = []
		for item in category_items:
			print type(item.dict)
			cat_items_dict.append(item.dict)
		category['items'] = cat_items_dict
		cat_json['category'].append(category)

	if fmt == 'json':
		resp = make_response(json.dumps(cat_json, indent=4, separators=(',', ': ')), 200)
		resp.headers['Content-Type'] = 'application/json'
	elif fmt == 'xml':
		resp = ""

	return resp

if (__name__ == '__main__'):
	app.secret_key = os.urandom(18) # required for sessions
	app.debug = True
	app.run(host='0.0.0.0', port=8000)