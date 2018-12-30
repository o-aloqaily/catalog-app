from flask import Flask, render_template, request
from flask import redirect, jsonify, url_for, flash, make_response
from database_setup import Category, Base, Item, User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, asc, desc
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from flask import session as login_session
import json
import httplib2
import requests
import random
import string

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secret.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog App"


engine = create_engine('sqlite:///catalogapp.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def main():
    latest_items = session.query(Item).order_by(
        desc(Item.created_at)).limit(10).all()
    return render_template('main.html', items=latest_items,
                           getCategoryTitle=getCategoryTitle)


#returns a category title given a category id.
def getCategoryTitle(category_id):
    return session.query(Category).filter_by(id=category_id).one().title


# The next two functions gconnect, gdisconnect was copied from the Auth&Auth lesson.
# from the Auth&Auth lesson, minor changes were made on them.
# gconnect, gdisconnect
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code, now compatible with Python3
    request.get_data()
    code = request.data.decode('utf-8')

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    # Submit request, parse response - Python3 compatible
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = jsonify('Current user is already connected.')
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    flash('Successfully signed in.')
    # return to the signinCallback function.
    return 'Success'


@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    result = requests.post('https://accounts.google.com/o/oauth2/revoke',
                           params={'token': access_token})

    if str(result.status_code) == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        flash('Successfully signed out.')
        return redirect(url_for('main'))
    else:
        # For whatever reason, the given token was invalid.
        flash('Failed to revoke token for given user.')
        return redirect('/')


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception:
        return None


@app.route('/category/<int:category_id>')
def showCategory(category_id):
    # shows the items of a category (when a category name is clicked)
    category_items = session.query(Item).filter_by(
        category_id=category_id).all()
    category_title = session.query(
        Category).filter_by(id=category_id).one().title
    return render_template(
            'category.html', category_items=category_items,
            category_id=category_id, category_title=category_title)


@app.route('/item/<int:item_id>')
def showItem(item_id):
    print(item_id)
    item = session.query(Item).filter_by(id=item_id).first()
    return render_template('item.html', item=item)


@app.route('/category/<int:category_id>/add', methods=["GET", "POST"])
def addItem(category_id):
    if 'username' not in login_session:
        flash('You need to be signed in to perform this action.')
        return redirect('/')

    category_title = session.query(
        Category).filter_by(id=category_id).one().title
    if request.method == 'GET':
        return render_template(
            'addItemForm.html', category_title=category_title)
    else:
        newItem = Item(
            title=request.form['title'],
            description=request.form['description'],
            category_id=category_id,
            user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash('New item was successfully added to {}.'.format(category_title))
        return redirect('/category/{}'.format(category_id))


@app.route('/item/<int:item_id>/edit', methods=["GET", "POST"])
def editItem(item_id):
    item = session.query(Item).filter_by(id=item_id).first()
    if (item is None):
        return 'No item was found'
    if 'username' not in login_session:
        flash('You do not have access to edit this item.')
        return redirect('/item/{}'.format(item_id))
    if item.user_id != login_session['user_id']:
        flash('You do not have access to edit this item.')
        return redirect('/item/{}'.format(item_id))

    if request.method == 'GET':
        categories = session.query(Category).all()
        return render_template(
            'editItemForm.html', categories=categories, item=item)
    else:
        item.title = request.form['title']
        item.description = request.form['description']
        item.category_id = request.form['category']
        session.commit()
        flash('All changes were saved.')
        return redirect('/item/{}'.format(item_id))


@app.route('/item/<int:item_id>/delete', methods=["POST"])
def deleteItem(item_id):
    itemToDelete = session.query(Item).filter_by(id=item_id).first()
    if (itemToDelete is None):
        return 'Error: item_id is incorrect.'
    if 'username' not in login_session:
        flash('You need to be signed in to perform this action.')
        return redirect('/')
    if itemToDelete.user_id != login_session['user_id']:
        flash('You do not have access to edit this item.')
        return redirect('/item/{}'.format(item_id))

    session.delete(itemToDelete)
    session.commit()
    flash('Successfully deleted {}'.format(itemToDelete.title))
    return redirect('/category/{}'.format(itemToDelete.category_id))


@app.route('/data.json')
def returnJSON():
    categories = session.query(Category).all()
    categories = [category.serialize for category in categories]
    for category in categories:
        print(category)
        items = session.query(Item).filter_by(category_id=category['id']).all()
        if items != []:
            category['items'] = [item.serialize for item in items]
    return jsonify(categories=categories)

# the following will inject all categories in the application
# to all templates in order to use them in the app header.
@app.context_processor
def inject_categories():
    categories_db = session.query(Category).all()
    return dict(categories=categories_db)


# the following will inject all login status in the application
# to all templates in order to use it in the app header.
# and whenever needed.
@app.context_processor
def inject_login_status():
    state = get_state_token()
    # return "The current session state is %s" % login_session['state']
    if 'username' in login_session:
        isLoggedIn = True
    else:
        isLoggedIn = False
    return dict(isLoggedIn=isLoggedIn, user_info=login_session, STATE=state)


# helper method for the last function, returns the state token
# for the user if the user is logged in, otherwise generates
# and returns a new one
def get_state_token():
    if 'state' in login_session:
        return login_session['state']
    else:
        state = ''.join(
            random.choice(string.ascii_uppercase + string.digits)
            for x in range(32))
        login_session['state'] = state
        return state


if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
