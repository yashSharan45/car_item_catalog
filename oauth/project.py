from flask import Flask 
from flask import jsonify, url_for
from flask import flash
from flask import render_template
from flask import request
from flask import redirect

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import AccessTokenCredentials

from sqlalchemy import create_engine
from sqlalchemy import asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base
from database_setup import Car
from database_setup import User
from database_setup import Item

import httplib2
import json
from flask import make_response

from flask import session as session_login
import random
import string

import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Car Menu Application"


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    session_login['state'] = state
    # return "The current session state is %s" % session_login['state']
    return render_template('login.html', STATE=state)


# Connect to Database and create database session
engine = create_engine('sqlite:///restaurantmenuwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# User Helper Functions


def createUser(session_login):
    newUser = User(name=session_login['username'], email=session_login[
                   'email'], picture=session_login['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=session_login['email']).one()
    return user.id


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    Menu_Item = session.query(Item).filter_by(id=menu_id).one()
    return jsonify(Menu_Item=Menu_Item.serialize)


@app.route('/restaurant/JSON')
def restaurantsJSON():
    restaurants = session.query(Car).all()
    return jsonify(restaurants=[r.serialize for r in restaurants])


# JSON APIs to view Car Information
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Car).filter_by(id=restaurant_id).one()
    items = session.query(Item).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


# Edit a menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editItem(restaurant_id, menu_id):
    if 'username' not in session_login:
        return redirect('/login')
    editedItem = session.query(Item).filter_by(id=menu_id).one()
    restaurant = session.query(Car).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['course']:
            editedItem.course = request.form['course']
        session.add(editedItem)
        session.commit()
        flash('Menu Item Successfully Edited')
        return redirect(url_for('menuDisplay', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)


# Delete a menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def delItem(restaurant_id, menu_id):
    if 'username' not in session_login:
        return redirect('/login')
    restaurant = session.query(Car).filter_by(id=restaurant_id).one()
    itemToDelete = session.query(Item).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('menuDisplay', restaurant_id=restaurant_id))
    else:
        return render_template('delItem.html', item=itemToDelete)


# Create a new restaurant
@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newCompany():
    if 'username' not in session_login:
        return redirect('/login')
    if request.method == 'POST':
        newCompany = Car(
            name=request.form['name'], user_id=session_login['user_id'])
        session.add(newCompany)
        flash('New Car %s Successfully Created' % newCompany.name)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newCompany.html')

# Create a new menu item
@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if 'username' not in session_login:
        return redirect('/login')
    restaurant = session.query(Car).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        newItem = Item(name=request.form['name'], description=request.form['description'], price=request.form[
                           'price'], course=request.form['course'], restaurant_id=restaurant_id, user_id=restaurant.user_id)
        session.add(newItem)
        session.commit()
        flash('New Menu %s Item Successfully Created' % (newItem.name))
        return redirect(url_for('menuDisplay', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)

# Edit a restaurant


@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    if 'username' not in session_login:
        return redirect('/login')
    editedRestaurant = session.query(
        Car).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedRestaurant.name = request.form['name']
            flash('Car Successfully Edited %s' % editedRestaurant.name)
            return redirect(url_for('showRestaurants'))
    else:
        return render_template('editRestaurant.html', restaurant=editedRestaurant)


# Show all restaurants
@app.route('/')
@app.route('/restaurant/')
def showRestaurants():
    restaurants = session.query(Car).order_by(asc(Car.name))
    if 'username' not in session_login:
		return render_template('publicrestaurants.html', restaurants=restaurants)
    else:	
		return render_template('restaurants.html', restaurants=restaurants)

	
# DISCONNECT - Revoke a current user's token and reset their session_login
@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    credentials = session_login.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del session_login['credentials']
        del session_login['gplus_id']
        del session_login['username']
        del session_login['email']
        del session_login['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
	response = make_response(redirect(url_for('showRestaurants')))
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Delete a restaurant
@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteCompany(restaurant_id):
    if 'username' not in session_login:
        return redirect('/login')
    restaurantToDelete = session.query(
        Car).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurantToDelete)
        flash('%s Successfully Deleted' % restaurantToDelete.name)
        session.commit()
        return redirect(url_for('showRestaurants', restaurant_id=restaurant_id))
    else:
        return render_template('deleteCompany.html', restaurant=restaurantToDelete)

# Show a restaurant menu


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def menuDisplay(restaurant_id):
    restaurant = session.query(Car).filter_by(id=restaurant_id).one()
    creator = getUserInfo(restaurant.user_id)	
    items = session.query(Item).filter_by(
        restaurant_id=restaurant_id).all()
    if 'username' not in session_login :
	    return render_template('publicmenu.html', items=items, restaurant=restaurant, creator=creator)
    else:
        return render_template('company.html', items=items, restaurant=restaurant, creator=creator)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != session_login['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
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
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
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
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = session_login.get('credentials')
    stored_gplus_id = session_login.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    session_login['credentials'] = credentials.access_token
	# return credential object
    credentials = AccessTokenCredentials(session_login['credentials'], 'user-agent-value')
    session_login['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    session_login['username'] = data['name']
    session_login['picture'] = data['picture']
    session_login['email'] = data['email']

    # See if a user exists, if it doesn't make a new one
    user_id = getUserID(session_login['email'])		
    if not user_id:		
	    user_id = createUser(session_login)		
    session_login['user_id'] = user_id	

    output = ''
    output += '<h1>Welcome, '
    output += session_login['username']
    output += '!</h1>'
    output += '<img src="'
    output += session_login['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % session_login['username'])
    print "done!"
    return output


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)	