import httplib2
import json
import requests

from flask import Flask
from flask import request, redirect, jsonify
from flask import url_for, make_response, render_template
from flask import session as login_session
from database_setup import Category, CategoryItem, User
from engine import Engine
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError



DATABASE = 'postgresql://linux:linux@127.0.0.1:5432/catalog'
app = Flask(__name__)
app.secret_key = 'this-is-a-secret'
engine = Engine(DATABASE)


'''
    Category resources
'''
# List of categories and lastest items
@app.route('/')
@app.route('/categories')
def index_resource():
    session = engine.get_session()

    categories = session.query(Category).all()
    categories = [item.serialize for item in categories if item]

    lastest_items = session.query(CategoryItem)
    lastest_items = lastest_items.order_by(CategoryItem.id.desc()).limit(10)
    lastest_items = [item.serialize for item in lastest_items if item]
    session.close()

    return render_template('categories.html',
                           categories=categories,
                           lastest_items=lastest_items)


@app.route('/categories/add', methods=['GET', 'POST'])
def category_add_resource():
    method = request.method.upper()
    if method == 'GET':
        return render_template('categoryNew.html')
    elif method == 'POST':
        session = engine.get_session()
        new_category = Category(
            title=request.form.get('category_title'),
            user_id=1
        )
        session.add(new_category)
        session.commit()
        session.close()
        return redirect('/categories')


@app.route('/categories/<category_id>/edit', methods=['GET', 'POST'])
def category_edit_resource(category_id):
    method = request.method.upper()
    session = engine.get_session()
    category = session.query(Category).filter_by(id=category_id).first()
    if method == 'GET':
        session.close()
        return render_template('categoryEdit.html', category=category)
    elif method == 'POST':
        category.title = request.form.get('category_title')
        session.commit()
        session.close()
        return redirect('/categories/{category_id}/items'.format(
            category_id=category_id)
        )


'''
    Item resources
'''
@app.route('/categories/<category_id>/items', methods=['GET'])
def category_items_resource(category_id):
    session = engine.get_session()
    categories = session.query(Category).all()
    categories = [item.serialize for item in categories]

    category = session.query(Category).filter_by(id=category_id).first()
    category = category.serialize

    items = session.query(CategoryItem).filter_by(category_id=category_id)
    items = [item.serialize for item in items]
    session.close()
    return render_template('items.html',
                           categories=categories,
                           category=category,
                           items=items)


@app.route('/categories/<category_id>/items/<item_id>', methods=['GET'])
def category_item_resource(category_id, item_id):
    session = engine.get_session()
    category = session.query(Category).filter_by(id=category_id).first()
    category = category.serialize
    item = session.query(CategoryItem).filter_by(id=item_id).first()
    item = item.serialize
    session.close()
    return render_template('itemView.html', category=category, item=item)


@app.route('/categories/<category>/items/add', methods=['GET', 'POST'])
def category_items_add_resource(category):
    method = request.method.upper()
    session = engine.get_session()
    if method == "GET":
        return render_template('itemNew.html', category_id=category)

    elif method == "POST":
        new_item = CategoryItem(
            title=request.form.get('item_title'),
            description=request.form.get('item_desc'),
            category_id=int(category))
        session.add(new_item)
        session.commit()
        session.close()
        return redirect('/categories/{category}/items'.format(
            category=category))


@app.route('/categories/<category>/items/<item_id>/edit',
           methods=['GET', 'POST'])
def category_items_put_resourcecategory(category, item_id):
    method = request.method.upper()
    session = engine.get_session()
    if method == "GET":
        item = session.query(CategoryItem).filter_by(id=item_id).first()
        item = item.serialize
        session.close()
        return render_template('itemEdit.html',
                               category_id=category,
                               item_id=item_id,
                               item=item)
    elif method == "POST":
        item = session.query(CategoryItem).filter_by(id=item_id).first()
        item.title = request.form.get('item_title')
        item.description = request.form.get('item_desc')
        session.commit()
        session.close()
        return redirect('/categories/{category}/items/{item}'.format(
            category=category, item=item_id)
        )


@app.route('/categories/<category_id>/items/<item_id>/delete',
           methods=['GET', 'POST'])
def category_items_delete_resource(category_id, item_id):
    method = request.method.upper()
    if method == "GET":
        return render_template('itemDelete.html',
                               category_id=category_id,
                               item_id=item_id)
    elif method == "POST":
        session = engine.get_session()
        session.query(CategoryItem).filter_by(id=item_id).delete()
        session.commit()
        session.close()
        return redirect('/categories/{category}/items'.format(
                        category=category_id))


'''
    Register and Authentication resources
'''
@app.route('/login', methods=['GET', 'POST'])
def login_resource():
    import uuid
    method = request.method.upper()
    if method == "GET":
        state = uuid.uuid4().hex
        login_session['state'] = state
        return render_template('login.html', state=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.form.get('state') != login_session['state']:
        return jsonify(msg='Invalid state parameter.', error=True), 401

    session = engine.get_session()
    google_user = User(
        name=request.form.get('name'),
        email=request.form.get('email'),
        photo=request.form.get('photo')
    )
    session.add(google_user)
    session.commit()

    login_session['user'] = google_user.name
    login_session['picture'] = google_user.photo
    login_session['email'] = google_user.email
    session.close()

    return jsonify(data="OK", error=False), 200


@app.route('/gdisconnect', methods=['POST'])
def gdisconnect():
    login_session.clear()
    return jsonify(error=False)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
