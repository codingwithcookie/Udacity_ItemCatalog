from flask import Flask, render_template, url_for, session, redirect, jsonify
from flask import request, make_response, flash
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from flask import session as login_session
from string import ascii_uppercase, digits
import random
import httplib2
import requests
from createDb import Base, Category, Item
from classes import WebPageViewModel, Item
from repository import Repository
import json
from flask import render_template

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('googleOAuth.json', 'r').read())['web']['client_id']


def SetWebPageVM():
    loginttext = ''
    loginlink = ''
    isLoggedIn = False
    if 'username' in login_session:
        loginttext = 'Welcome, ' + login_session['username']
        loginlink = '/logout'
        isLoggedIn = True
    else:
        loginttext = 'Login'
        loginlink = '/login'
    webPageVM = WebPageViewModel(loginttext, loginlink, isLoggedIn)
    return webPageVM


@app.route('/')
def home_page():
    repo = Repository()
    items = repo.getAllItems()
    return render_template('home.html', WebPage=SetWebPageVM(), items=items)


@app.route('/json')
def json_response():
    jsonitems = []
    repo = Repository()
    items = repo.getAllItems()
    for item in items:
        jsonitems.append(
            {'id': item.id,
             'name': item.name,
             'description': item.description,
             'category': item.categoryid})
    return jsonify(jsonitems)


@app.route('/json/<int:itemid>')
def json_item_response(itemid):
    jsonitems = []
    repo = Repository()
    item = repo.getItemById(itemid)
    jsonitems.append(
        {'id': item.id,
         'name': item.name,
         'description': item.description,
         'category': item.categoryid})
    return jsonify(jsonitems)


@app.route('/login')
def login_page():
    state = ''.join(random.choice(ascii_uppercase + digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state, WebPage=SetWebPageVM())


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('googleOAuth.json', scope='')
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

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;">'
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/logout')
def logout():
    access_token = login_session['access_token']
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token='
    url += login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(
            json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect("/", code=200)
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return redirect("/", code=200)


@app.route('/item/<int:itemid>/')
def item_page(itemid):
    repo = Repository()
    item = repo.getItemById(itemid)
    return render_template('item.html', WebPage=SetWebPageVM(), item=item)


@app.route('/item/add')
def add_item_page():
    webPage = SetWebPageVM()
    if webPage.isLoggedIn:
        return render_template('additem.html', WebPage=webPage)
    return redirect('/')


@app.route('/item/postadd', methods=['POST'])
def post_add_item():
    webPage = SetWebPageVM()
    if webPage.isLoggedIn:
        repo = Repository()
        repo.addItemToDatabase(
            request.form['name'],
            request.form['description'],
            request.form['category'],
            login_session['username'])
        return redirect('/')
    return render_template('additem.html', WebPage=webPage)


@app.route('/item/edit/<int:itemid>/')
def edit_item_page(itemid):
    webPage = SetWebPageVM()
    if webPage.isLoggedIn:
        repo = Repository()
        item = repo.getItemById(itemid)
        return render_template(
            'edititem.html', edititem=item,
            WebPage=webPage)
    return redirect('/')


@app.route('/item/postedit', methods=['POST'])
def post_edit_item():
    webPage = SetWebPageVM()
    if webPage.isLoggedIn:
        repo = Repository()
        itemid = request.form['itemid']
        item = repo.getItemById(itemid)
        if item.user == login_session['username']:
            item.name = request.form['name']
            item.description = request.form['description']
            item.categoryid = request.form['category']
        return redirect('/')
    return render_template('additem.html', WebPage=webPage)


@app.route('/item/delete/<int:itemid>/')
def delete_item_page(itemid):
    webPage = SetWebPageVM()
    repo = Repository()
    item = repo.getItemById(itemid)
    if webPage.isLoggedIn:
        if item.user == login_session['username']:
            repo.deleteFromDatabase(item)
    return redirect('/')


if __name__ == '__main__':
    app.secret_key = '7HLYF4PNPWE1LPFB8PO1YQDBCGNSIURP'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
